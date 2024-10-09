# Frequenz Common API Release Notes

Update of the `PaginationParams` struct.

## Upgrading

- `PaginationParams` has been changed so that the `page_size` and `page_token`
  fields are now mutually exclusive.

- A new component category `COMPONENT_CATEGORY_HVAC` has been added to the API
  to represent HVAC (Heating, Ventilation, and Air Conditioning) systems.

- Additional information for energy metric

- Generalize Energy message documentation for broader market use

- Add Power message to represent Power in MW

## Bug Fixes

- Fix a dependency issue by pinning the `grpcio` version and related libraries.
- Fixed a wrong documentation comment for `COMPONENT_CATEGORY_UNSPECIFIED`.
