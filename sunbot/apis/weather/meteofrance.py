"""Meteo France Handler"""

import logging
from sunbot.core.api_handler import APIHandler


class MeteoFranceHandler(APIHandler):
    """Meteo France API handler. This handler provides some methods to:
    - get current vigilance state for any France department
    - ... (see for future update)
    """

    def __init__(self, **kwargs) -> None:
        """_summary_
        """
        super().__init__(domain_name="public-api.meteofrance.fr", auth_mode="jwt", **kwargs)

    def get_vigilance_state(self, dep_num: int) -> dict:
        """Get vigilance state for the specified France department

        Returns
        -------
        dict
            _description_
        """
        response = self.request(resource_path="/public/DPVigilance/v1/textesvigilance/encours")

        data = self.get_data(
            response=response,
            targets={"text_bloc_items": "domains"},
            max_depth=1
        )

        for domain in data["domains"]:
            if domain["domain_id"] == str(dep_num):
                return domain
        logging.error("Unknown department number (%d)", dep_num)
        return None
