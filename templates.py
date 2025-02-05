# Create template for generating cypher code using LLM

def generate_template(schema, question):
	schema = schema
	question = question

	template = """
	Task: Generate a Cypher statement to query the graph database.

	Instructions:
	Use only relationship types and properties provided in schema.
	Do not use other relationship types or properties that are not provided.
	You can match the different relationships to come up with the answer to the question
	If a name is given, check if any property name contains the given name

	schema:
	{schema}

	Examples:
	1. Question: what could be the environmental risk factors for Diabetes?
		Cypher: MATCH (e:exposure)-[:exposure_disease]-(d:disease)
		WHERE d.node_name CONTAINS 'diabetes'
		RETURN e.node_name AS Environmental_Risk_Factor, d.node_name AS Disease

	2. Question: What could be the environmental risk factors for Cardiovascular disease?
		Cypher: MATCH (e:exposure)-[:exposure_disease]-(d:disease)
		WHERE d.node_name CONTAINS 'cardiovascular disease'
		RETURN e.node_name AS Environmental_Risk_Factor, d.node_name AS Disease

	3. Question: Which occupational hazards are linked to an increased risk of respiratory diseases?
		Cypher: MATCH (e:exposure)-[:exposure_disease]-(d:disease)
		WHERE d.node_name CONTAINS 'respiratory'
		RETURN e.node_name AS Environmental_Risk_Factor, d.node_name AS Disease

	4. Question: What are the most common secondary diseases in patients with diabetes or obesity?
		Cypher: MATCH (d1:disease)-[:disease_disease]-(d2:disease),
				(d1)-[:disease_protein]-(p:gene__protein)
		WHERE d1.node_name CONTAINS 'diabetes' OR d1.node_name CONTAINS 'obesity'
		RETURN d1.node_name AS Primary_Disease, d2.node_name AS Secondary_Disease, p.node_name AS Protein

	5. Question: Explore the relationship between environmental exposures and diseases affecting reproduction
		Cypher: MATCH (e:exposure)-[:exposure_disease]-(d:disease),
				(e)-[:exposure_protein]-(p:gene__protein),
				(d)-[:disease_protein]-(p)
		WHERE d.node_name CONTAINS 'infertility' OR d.node_name CONTAINS 'ovary' or  d.node_name CONTAINS 'prostate'
		RETURN e.node_name AS Exposure, d.node_name AS Disease, p.node_name AS Protein

	Note: Do not include explanations or apologies in your answers.
	Do not answer questions that ask anything other than creating Cypher statements.

	Question: {question}"""

	return template
