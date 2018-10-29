DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'lab2ai64'
DB_NAME = 'baseball'
LAB2AI_DB_NAME = 'lab2ai_article'
DB_PORT = 3307

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'lab2ai64',
    'port': 3307,
    'db': 'baseball',
    'charset': 'utf8mb4'
}

LAB2AI_DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'lab2ai64',
    'port': 3307,
    'db': 'lab2ai_article',
    'charset': 'utf8mb4'
}

GSPREAD_DICT = {
    "type": "service_account",
    "project_id": "lab2ai-project",
    "private_key_id": "5a8eef99b67f412fcc69c64135e4bf09969e6dec",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCHwoEeBWdO0KGI\nxcnfAJTVTOalL9saE31WNZYbttGk9LaS8YaODZG5sgkpr53P8VsyCnyouueBUPNs\n/VNkjxPbS4ufCrPJRIG7qKOxLRkYp5YdrR6K/VIr+qtbAtrGS7YQNfPDJJUrWNF1\n4J4nyYAGghhVoZsS/22we549/Ox7fDIA9z4bDlZhlw1gQaOuDZ7oTVqqu5s/iLwv\nZO5J/RVV30iTgJLDaCgWnbUMy7O03crLfy+J7oJBTqsjoXT4giz7z59WuM9xlUxC\nWtPrInuoYoC4gIDkMckBZ5lQTUNkfi9qIRLBYVARcQhLOyKiYwpp4D9ur1Irxln3\nxnI6QdRDAgMBAAECggEAEC4GOrsPd5KLLe8krVyMYGosiD4OhtURIwJ6mWL4frML\nmge0WZ8UYbqY4kxOf/Hr7ygreJCN9sOHFNORlMfYk1I1mbF/gS/rpknloxVqNZ4D\ng2tBMJ9wTlLZs/HAe9GaKTnE4NpYojSRAijQWz2QnItKCyqaKMbNyTLHxpYrjlaF\nIEZP11XjMgoj8QfKVOBrp1k3mszBqE6wktfYALB1atlc5Mrr3hclIbCfXeMVR/mJ\n7smX7ZoIvLcV4B6hWQ4R/2+JbPV/BR1z9pIp39naTyj7kc+O1SF6cd0xKH6qQ7mn\nOzzBOVQTL+pfCDArfdO9p78OeKnQsKYNw+TX1r+zgQKBgQC/o+KZSyDR3o9rWFYy\n8T2cNtF93V8GzA3GSSBU88k+censmwZIIdMOjjAzveQ7s94FMAxOKDwl7dzqgvLR\nXC3g4i7kJL1C1fE+PaknTcsj/Y2N8KaTRjumxbYvMag46Y9/g6qq8rvkQtFABkwH\naYrNvjvo7K/ZFn+Trnllu3FwiQKBgQC1WliNHbPWPCWXLTSSq9qRmlZmw/RANF1j\nzP7CT4t6ZfcHQFP85dT455g1wSU+1IzdBS1DYq5lBQz7CcQt5ASS+jNGoO5O/dJB\nR1sLYSyIOsMdxzlv9E3mKnyctrrNC7daLG2bQydqGmTob8l9hwHQQ+qUfCHzzUxr\nljds9OizawKBgQCvhbIQhw/7SKYBQnpI1E2Cm27KogvcFN704ps7U8HZcMo5DE/3\nlwtRBIg/i8fTqs1J4RUULKPSdYbmP6OYf54BoAgkq0WxRnRbdmxMdGL/hsa031oh\n/6y49dMEbK3P2pO0zepuAj53NX+j7WCLVW5tPLRwhQAWjBWzNJU5yTGASQKBgCD+\nPcv2kmgwaxpU1BK3Bz2kGYH6tm4T2MW2XsbVF+f9svJzxpPk8FkUMUHeULtcigAP\n2AtBYb7pK1JklXdP23Et6bQ4xQJD9UOBCtRIKoTiQ+sf+pgelyl/o0oTiGqTbhkO\nqiYsEnigMqmC5OJcdH0CTiQTbU3glL2iB5Vf/RHfAoGAC0eP3Ckz5GpHaAk9pnAq\nO6oCqwCWr6gaJ+sawoXuouAtvArspM9bjAz6Kn+r72VPEQbwuoNyc4UJN3IdpoPc\noo3uvE1lHBVvBUVrYqIjpl11ulqZqN1aiW5P2AuH5QyeJXaeOX5i5K/otdu8X0VU\nfFuE7woNevllcT43MxyQxqI=\n-----END PRIVATE KEY-----\n",
    "client_email": "lab2ai-gspread@lab2ai-project.iam.gserviceaccount.com",
    "client_id": "107669282039947980804",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/lab2ai-gspread%40lab2ai-project.iam.gserviceaccount.com"
}
GSPREAD_SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
GSPREAD_URL = 'https://docs.google.com/spreadsheets/d/1dp7PoDgaX9s7rWjf4hU_K49EiiDNwcT1p2xMMmgDjcA/edit?usp=sharing'