### 📤 HTTP Protocol Client: Building Requests from Scratch

This project is a custom **HTTP client** meticulously implemented from the ground up using **Python socket programming**. It demonstrates a deep understanding of network protocols by manually constructing and parsing HTTP requests and responses. The client features both a robust console interface for direct command-line interaction and a user-friendly GUI for intuitive request building.

*Showcases foundational network programming, HTTP protocol understanding, and versatile interface design.*

![image](gui.png)
### More:

**Key Technical Achievements & Demonstrated Skills:**
*   **Low-Level Socket Programming:** Directly managed TCP/IP sockets to establish connections and handle data exchange, demonstrating a core understanding of how web communication operates at a fundamental level.
*   **Full HTTP Protocol Implementation:** Manually constructed and parsed HTTP requests (e.g., GET, POST methods) including handling custom headers and body payloads, adhering closely to protocol specifications.
*   **Dual Interface Design:** Developed both a command-line interface (CLI) for powerful, scriptable interactions and a graphical user interface (GUI) for enhanced usability, showcasing adaptability in UI/UX development.
*   **Robust Request & Response Handling:** Implemented logic to reliably send requests to various endpoints and efficiently process server responses, including status codes and content.
*   **Python-driven Development:** Leveraged Python for its versatility in rapid prototyping and network programming, proving proficiency in building functional applications.

This project highlights a strong foundation in **network programming**, **HTTP protocol understanding**, and **practical application development**.

## Instructions:
### Command-Line Interface (CLI):

To launch the console client, simply run `request_console.py` and submit requests in the following format:

```
post http://cubadebate.cu:84 {'header1': 'value1', 'header2': 'value2'} (body content)
```
> **Important:** Do not include additional `{}` characters in the command, as they are reserved by the parsing regex to delineate specific command fragments.

Body content can also be sent without specifying headers:

```
get http://cubadebate.cu:84 (body content)
```
> **Note:** The first two parameters (HTTP method and URL) are always required.

#### Graphical User Interface (GUI):

To launch the GUI, simply run `request_gui.py`, which will display the interface:

![image](gui.png)

> Each input field provides an example to guide its use. Once the 'Send' button is clicked to dispatch the request, the results will be displayed in the console where the `.py` script was originally launched.
