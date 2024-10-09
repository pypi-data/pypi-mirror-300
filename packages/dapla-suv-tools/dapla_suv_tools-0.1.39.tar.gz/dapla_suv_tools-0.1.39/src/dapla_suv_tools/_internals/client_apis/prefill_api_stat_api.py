from typing import Optional
import json

from dapla_suv_tools._internals.integration.api_client import SuvApiClient, PREFILL_API_BASE_URL
from dapla_suv_tools._internals.util.decorators import result_to_dict
from dapla_suv_tools._internals.util.operation_result import OperationResult
import dapla_suv_tools._internals.util.constants as constants
from dapla_suv_tools._internals.util.suv_operation_context import SuvOperationContext
from dapla_suv_tools._internals.util.validators import ra_nummer_validator

client = SuvApiClient(base_url=PREFILL_API_BASE_URL)


@result_to_dict
@SuvOperationContext(validator=ra_nummer_validator)
def get_prefill_info_for_skjema(
        self,
        *,
        ra_nummer: str,
        versjon: int,
        periode_aar: int,
        periode_type: str,
        periode_nr: Optional[int],
        context: SuvOperationContext
) -> OperationResult:
    """
    Fetches prefill information for a given combination of skjema-identifiers and periode-identifiers.

    :param ra_nummer: str, required  Ra-number of the skjema
    :param versjon:  int, required   Version indicator of the skjema
    :param periode_aar: int, required  The year of the period
    :param periode_type: str, required  The type of period
    :param periode_nr: int, optional   The number of the period.  Not required for annual surveys.
    :param context:
    :return:
    """
    try:
        query = f"ra_nummer={ra_nummer}&versjon={versjon}&periode_aar={periode_aar}&periode_type={periode_type}"
        if periode_nr:
            query += f"&periode_nummer={periode_nr}"
        content = client.get(path=f"{constants.PREFILL_API_STAT_PATH}/skjema?{query}", context=context)
        content_json = json.loads(content)
        context.log(message=f"Fetched prefill-info for: {ra_nummer}-{versjon} ({periode_aar}-{periode_type}-{periode_nr}")
        return OperationResult(
            value=content_json, log=context.logs()
        )
    except Exception as e:
        context.set_error(f"Failed to fetch for {ra_nummer}-{versjon} ({periode_aar}-{periode_type}-{periode_nr}", e)

        return OperationResult(
            success=False, value=context.errors(), log=context.logs()
        )