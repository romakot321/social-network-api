from pydantic import BaseModel, computed_field


class Caption(BaseModel):
    text: str


class Image(BaseModel):
    class Candidate(BaseModel):
        url: str

    candidates: list[Candidate]


class InstagramPost(BaseModel):
    pk: str
    code: str
    like_count: int | None = None
    comment_count: int | None = None
    play_count: int | None = None
    image_versions2: Image
    caption: Caption | None = None
    taken_at: int

    @computed_field
    @property
    def url(self) -> str:
        return f"https://www.instagram.com/p/{self.code}"


class InstagramAccountCookies(BaseModel):
    csrftoken: str
    datr: str
    ds_user_id: str
    ig_did: str
    ig_nrcb: str = "1"
    mid: str
    ps_l: str = "1"
    ps_n: str = "1"
    rur: str
    sessionid: str
    wd: str = "1980x1024"
