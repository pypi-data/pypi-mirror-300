
# byAd12-library - v1.1

**byAd12-library** helps you doing a ICMP (ping) attack to a specific target.
Feel free to open an issue or a pull request in the repository.

## Project

- **PyPi**: [https://pypi.org/project/byAd12-library/](https://pypi.org/project/byAd12-library/)
- **Installation**: 
  ```bash
  pip install byAd12-library
  ```

## Author

- **Website**: [https://byAd12.pages.dev](https://byAd12.pages.dev)
- **Email**: [adgimenezp@gmail.com](mailto:adgimenezp@gmail.com)

## Functions

- `Ping_Flood_(IPv4)`
Sends massive pings (ICMP messages) to a target (local or server) using IPv4.

- `byAd12_Info_()`
Provides information about the library.

## Required Dependencies

- **pip install threading**
- **pip install ping3**

## Example

```python
from byAd12_library import Ping_Flood_, byAd12_Info_


Ping_Flood_("192.168.1.1") # Send massive pings


byAd12_Info_() # Get information about the library
```