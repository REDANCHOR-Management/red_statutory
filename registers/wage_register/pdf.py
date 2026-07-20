"""
Generate Wage Register PDF.
"""

from .query import get_rows

def generate(filters):
    rows = get_rows(filters)
    # render template
    # convert to pdf
    raise NotImplementedError
