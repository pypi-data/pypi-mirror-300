from __future__ import annotations

import contextlib
import logging
from collections.abc import Iterator
from operator import itemgetter

import itkdb
from itkdb.models.component import Component as ITkDBComponent

from module_qc_database_tools.typing_compat import ProdDBComponent

log = logging.getLogger(__name__)


def get_component(client, serial_number) -> (ProdDBComponent, str):
    """
    Get component information using serial number.

    Args:
        client (:obj:`itkdb.Client`): itkdb client to query for component information
        serial_number (:obj:`str`): serial number of component to get information for

    Returns:
        component (:obj:`dict`): information about the component from prodDB
    """
    try:
        component = client.get("getComponent", json={"component": serial_number})
    except itkdb.exceptions.BadRequest as exc:
        msg = "An unknown error occurred. Please see the log."
        with contextlib.suppress(Exception):
            message = exc.response.json()
            if "ucl-itkpd-main/getComponent/componentDoesNotExist" in message.get(
                "uuAppErrorMap", {}
            ):
                msg = f"component with {serial_number} not in ITk Production DB."

        raise ValueError(msg) from exc

    current_stage = (component.get("currentStage") or {}).get("code")
    if not current_stage:
        msg = f"component with {serial_number} does not have a current stage. Something is wrong with this component in ITk Production Database."
        raise ValueError(msg)

    return (component, current_stage)


def get_children(
    client, component: ProdDBComponent, *, component_type
) -> Iterator[ProdDBComponent]:
    """
    Get children for component by ID matching the component type from Local DB.

    !!! note

        This returns a generator.

    Args:
        client (:obj:`itkdb.Client`): itkdb client to query for parent-child relationship
        component (:obj:`dict`): the top-level component to recursively get the children of
        component_type (:obj:`str`): the component type code to filter children by

    Returns:
        children (:obj:`iterator`): generator of localDB components matching the component type
    """

    def _recursive(
        component: ITkDBComponent, *, component_type
    ) -> Iterator[ProdDBComponent]:
        if (component._data.get("componentType") or {}).get("code") == component_type:  # pylint: disable=protected-access
            yield component._data  # pylint: disable=protected-access

        for child in component.children:
            yield from _recursive(child, component_type=component_type)

    # walk through structure
    component_model = ITkDBComponent(client, component)
    component_model.walk()

    yield from _recursive(component_model, component_type=component_type)


def get_reference_iv_testRuns(
    client, reference_components, *, reference_stage, reference_testType
):
    """
    Get reference test runs for the referenced components in the reference stage.

    This will grab the latest testRun based on the most recently created date in prodDB.

    !!! warning "do not use `date`"

        Measurements have a datetime when measurement was performed.
        Analyses have a datetime when analysis was performed.

        If an (re)analysis is done and uploaded to prodDB:

        - localDB uses the "analysis record entry" as the `date`
        - webApp uses the "measurement date" as the `date`

        If one is trying to identify the latest test result, one
        cannot rely on the `date` if it was done with webApp (but one
        can rely on the `date` if done with localDB).

    Args:
        client (:obj:`itkdb.Client`): itkdb client to query for test run information
        reference_components (:obj:`list` of :obj:`dict`): list of localDB components to use to pull reference test runs from
        reference_stage (:obj:`str`): the stage for where the tests should be located
        reference_testType (:obj:`str`): the type of tests to use as reference

    Returns:
        reference_iv_testRuns (:obj:`list` of `:obj:`dict`): list of reference test runs corresponding to one test run for each reference component provided
    """

    reference_iv_testRuns = []

    for ref_component in reference_components:
        # for each component, build a list of tests with state=ready, sorting by the 'date' of the test itself
        try:
            ref_testRuns = sorted(
                client.get(
                    "listTestRunsByComponent",
                    json={
                        "filterMap": {
                            "serialNumber": ref_component["serialNumber"],
                            "stage": [reference_stage],
                            "testType": [reference_testType],
                            "state": ["ready"],
                        }
                    },
                ),
                # warning: do not use 'date'
                # - measurements have a datetime when measurement was performed
                # - analyses have a datetime when analysis was performed
                #
                # if an (re)analysis is done and uploaded to prodDB
                # - localDB uses the "analysis record entry" as the 'date'
                # - webApp uses the "measurement date" as the 'date'
                #
                # If one is trying to identify the latest test result, one
                # cannot rely on the 'date' if it was done with webApp (but one
                # can rely on the 'date' if done with localDB).
                key=itemgetter("cts"),
            )
        except itkdb.exceptions.BadRequest as exc:
            msg = "An unknown error occurred. Please see the log."
            raise ValueError(msg) from exc

        if not ref_testRuns:
            reference_iv_testRuns.append(None)
            continue

        # pylint: disable=duplicate-code
        if len(ref_testRuns) != 1:
            log.warning(
                "Multiple test runs of %s were found for %s. Choosing the latest tested.",
                reference_testType,
                ref_component["serialNumber"],
            )

        # get the last one
        testRun_id = ref_testRuns[-1]["id"]

        try:
            ref_testRun = client.get("getTestRun", json={"testRun": testRun_id})
        except itkdb.exceptions.BadRequest as exc:
            msg = "An unknown error occurred. Please see the log."
            with contextlib.suppress(Exception):
                message = exc.response.json()
                if "ucl-itkpd-main/getTestRun/testRunDaoGetFailed" in message.get(
                    "uuAppErrorMap", {}
                ):
                    msg = f"test run with id={testRun_id} for {ref_component['serialNumber']} not in ITk Production DB."

            raise ValueError(msg) from exc

        reference_iv_testRuns.append(ref_testRun)

    return reference_iv_testRuns
