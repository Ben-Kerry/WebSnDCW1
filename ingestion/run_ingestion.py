from ingestion.loaders.api_loader import ApiLoader


if __name__ == "__main__":
    loader = ApiLoader()
    print("Ingestion runner ready.")
    print(loader.get("teams"))