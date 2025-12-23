# backend/gn_module_quadrige/build_query.py
from gql import gql


def build_extraction_query(program_name: str, filter_data: dict):
    """
    Construit une mutation executeResultExtraction conforme à l'API Quadrige.
    """

    # --- validations ---
    fields = filter_data.get("fields")
    if not fields or not isinstance(fields, list):
        raise ValueError("Liste de champs 'fields' manquante ou invalide")

    monitoring_location = filter_data.get("monitoringLocation")
    if not monitoring_location:
        raise ValueError("monitoringLocation manquante")

    fields_graphql = ", ".join(fields)

    # --- périodes (OPTIONNELLES) ---
    periods_graphql = ""
    if filter_data.get("startDate") and filter_data.get("endDate"):
        periods_graphql = f"""
        periods: [{{
          startDate: "{filter_data['startDate']}"
          endDate: "{filter_data['endDate']}"
        }}]
        """

    filter_name = filter_data.get("name", "Extraction données")

    query = f"""
    mutation {{
      executeResultExtraction(
        filter: {{
          name: "{filter_name}"
          extractionFilterVersion: "2"
          fields: [{fields_graphql}]
          {periods_graphql}
          mainFilter: {{
            program: {{
              ids: ["{program_name}"]
            }}
            monitoringLocation: {{
              text: "{monitoring_location}"
            }}
          }}
        }}
      ) {{
        id
        name
        startDate
        status
      }}
    }}
    """

    print("\\n[QUADRIGE][GRAPHQL][DATA EXTRACTION]")
    print(query)
    print("----------------------------------\\n")

    return gql(query)