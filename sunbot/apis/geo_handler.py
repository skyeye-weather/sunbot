from sunbot.core import APIHandler


class GeoFrHandler(APIHandler):
    """Geo API Handler"""

    def __init__(self) -> None:
        super().__init__(domain_name="geo.api.gouv.fr", auth_mode="no")

    def get_department(self, location_name : str) -> dict:
        """ Get department number for the speacified location

        Parameters
        ----------
        location_name : str
            name of the location for which to retrieve the department number

        Returns
        -------
        dict
            dict representing the location department with name and code keys
        """
        response = self.request(
            resource_path="communes",
            request_args={
                "nom": location_name,
                "fields": "departement",
                "limit": 1,
            }
        )

        department = self.get_data(
            response=response,
            targets={
                "departement/code": "id",
                "departement/nom": "name",
            }
        )
        return department
