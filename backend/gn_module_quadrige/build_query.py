# backend/gn_module_quadrige/build_query.py
from gql import gql


def build_extraction_query(program_name: str, filter_data: dict):
    fields = filter_data.get("fields")
    if not fields or not isinstance(fields, list):
        raise ValueError("Liste de champs 'fields' manquante ou invalide")

    periods = []
    if filter_data.get("startDate") and filter_data.get("endDate"):
        periods.append({
            "startDate": filter_data["startDate"],
            "endDate": filter_data["endDate"],
        })

    fields_graphql = ", ".join(fields)

    periods_graphql = ""
    if periods:
        periods_graphql = f"""
        periods: [{{
          startDate: "{periods[0]['startDate']}"
          endDate: "{periods[0]['endDate']}"
        }}]
        """

    return gql(f"""
    mutation {{
      executeResultExtraction(
        filter: {{
          name: "{filter_data.get('name', 'Extraction données')}"
          fields: [{fields_graphql}]
          {periods_graphql}
          mainFilter: {{
            program: {{
              ids: ["{program_name}"]
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
    """)
