# DBnomics Data Model

In DBnomics, once data has been downloaded from providers, it is converted in a common format: the DBnomics data model.

This Python package provides:

- model classes defining DBnomics entities (provider, dataset, series, etc.) with their business logic and validation rules
- a data storage abstraction to load and save those entities
- adapters implementing the data storage abstraction (e.g. `dbnomics_data_model.storage.adapters.filesystem`)

## Documentation

Please read <https://db.nomics.world/docs/data-model/>
