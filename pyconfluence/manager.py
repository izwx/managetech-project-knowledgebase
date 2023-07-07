from atlassian import Confluence

class ConfluenceManager:
    def __init__(self, server_url : str, email_address : str, api_token : str) -> None:
        self.server_url = server_url
        self.email_address = email_address
        self.api_token = api_token
        self.confluence = Confluence(
            url=server_url,
            username=email_address,
            password=api_token,
            cloud=True
        )

    def __str__(self) -> str:
        return f"Confluence | {self.server_url} | {self.email_address}"

    def get_space(self, space_key : str) -> dict:
        space_info = self.confluence.get_space(space_key, expand='history')
        return space_info

    def get_pages(self, space_key : str) -> list:
        pages = []
        idx = 0
        while idx == 0 or len(pages) == idx * 50:
            pages += self.confluence.get_all_pages_from_space(space_key, start = idx * 50, expand="body.view")
            idx += 1 
        
        return pages

    def get_page_history(self, page_id : str) -> dict:
        his = self.confluence.get_content_history(page_id)
        return his

