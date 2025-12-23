from gql import gql


def build_extraction_query(program_name: str, filter_data: dict):
    """
    Construit la mutation GraphQL executeResultExtraction conforme à l'API Quadrige.

    Obligatoire :
      - fields (liste non vide)
      - program_name
      - monitoringLocation (injectée par la route via last_filter)

    Optionnel :
      - periods (startDate + endDate)
    """

    # --- Validations ---
    fields = filter_data.get("fields")
    if not fields or not isinstance(fields, list):
        raise ValueError("Liste de champs 'fields' manquante ou invalide")

    if not program_name:
        raise ValueError("Nom de programme manquant")

    monitoring_location = filter_data.get("monitoringLocation")
    if not monitoring_location:
        raise ValueError("monitoringLocation manquante dans filter_data")

    # --- Champs ---
    fields_graphql = ", ".join(fields)

    # --- Périodes (optionnelles) ---
    periods_graphql = ""
    start_date = filter_data.get("startDate")
    end_date = filter_data.get("endDate")

    if start_date and end_date:
        periods_graphql = f"""
        periods: [{{
          startDate: "{start_date}"
          endDate: "{end_date}"
        }}]
        """

    # --- Nom du filtre ---
    filter_name = filter_data.get("name", "Extraction données")

    # --- Mutation GraphQL ---
    return gql(f"""
    mutation {{
      executeResultExtraction(
        filter: {{
          name: "{filter_name}"
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
    """)
