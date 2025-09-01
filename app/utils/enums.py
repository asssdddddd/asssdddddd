from enum import Enum


class Role(str, Enum):
    unknown = "unknown"
    worker = "worker"
    employer = "employer"


class ListingType(str, Enum):
    worker_profile = "worker_profile"
    job_post = "job_post"


class ListingStatus(str, Enum):
    draft = "draft"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    posted = "posted"


class Channel(str, Enum):
    jobs = "jobs"
    workers = "workers"
