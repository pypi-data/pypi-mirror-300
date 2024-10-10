from __future__ import annotations

import logging
from collections.abc import Iterator

from bson import ObjectId

from module_qc_database_tools.typing_compat import LocalDBComponent

log = logging.getLogger(__name__)


def get_component(database, serial_number) -> (LocalDBComponent, str):
    """
    Get component information using serial number.

    Args:
        database (:obj:`pymongo.database.Database`): mongoDB database to query for component information
        serial_number (:obj:`str`): serial number of component to get information for

    Returns:
        component (:obj:`dict`): information about the component from localDB
    """
    component = database.component.find_one({"serialNumber": serial_number})
    if not component:
        msg = f"component with {serial_number} not in your localDB"
        raise ValueError(msg)

    component_id = str(component["_id"])

    component_qcstatus = database.QC.module.status.find_one({"component": component_id})
    if not component_qcstatus:
        msg = f"component with {serial_number} does not have any QC status. Something went wrong in your localDB."
        raise ValueError(msg)

    return (component, component_qcstatus["currentStage"])


def get_children(
    database, component: LocalDBComponent, *, component_type
) -> Iterator[LocalDBComponent]:
    """
    Get (unique!) children for component by ID matching the component type from Local DB.

    !!! note

        This returns a generator.

    Args:
        database (:obj:`pymongo.database.Database`): mongoDB database to query for parent-child relationship
        component (:obj:`dict`): the top-level component to recursively get the children of
        component_type (:obj:`str`): the component type code to filter children by

    Returns:
        children (:obj:`iterator`): generator of localDB components matching the component type
    """

    def _recursive(
        database, component_id: str, *, component_type
    ) -> Iterator[LocalDBComponent]:
        component = database.component.find_one({"_id": ObjectId(component_id)})
        yielded = set()

        if component.get("componentType") == component_type:
            yield component

        for child_id in database.childParentRelation.find(
            {"parent": component_id}
        ).distinct("child"):
            # yield from get_children(database, child_id, component_type=component_type)
            for child in _recursive(database, child_id, component_type=component_type):
                if child["_id"] in yielded:
                    continue
                yield child
                yielded.add(child["_id"])

    component_id = str(component["_id"])
    yield from _recursive(database, component_id, component_type=component_type)


def get_reference_iv_testRuns(
    database, reference_components, *, reference_stage, reference_testType
):
    """
    Get reference test runs for the referenced components in the reference stage.

    This will grab the latest testRun based on the most recently modified date in localDB.

    Args:
        database (:obj:`pymongo.database.Database`): mongoDB database to query for test run information
        reference_components (:obj:`list` of :obj:`dict`): list of localDB components to use to pull reference test runs from
        reference_stage (:obj:`str`): the stage for where the tests should be located
        reference_testType (:obj:`str`): the type of tests to use as reference

    Returns:
        reference_iv_testRuns (:obj:`list` of `:obj:`dict`): list of reference test runs corresponding to one test run for each reference component provided
    """
    reference_iv_testRuns = []

    for ref_component in reference_components:
        ref_testRuns = list(
            database.QC.result.find(
                {
                    "$and": [
                        {
                            "$or": [
                                {"stage": reference_stage},
                                {"currentStage": reference_stage},
                            ]
                        },
                        {
                            "component": str(ref_component["_id"]),
                            "testType": reference_testType,
                        },
                    ]
                },
                sort={"sys.mts": 1},
            )
        )

        # pylint: disable=duplicate-code
        if len(ref_testRuns) != 1:
            log.warning(
                "Multiple test runs of %s were found for %s. Choosing the latest tested.",
                reference_testType,
                ref_component["serialNumber"],
            )

        # get the last one
        ref_testRun = ref_testRuns[-1]
        reference_iv_testRuns.append(ref_testRun)

    return reference_iv_testRuns
