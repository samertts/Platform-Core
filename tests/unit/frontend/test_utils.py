"""
Tests for NHDOS Frontend Utilities
"""

import sys

sys.path.insert(0, "/tmp")

from datetime import datetime

from platform_core.frontend.utils import (camel_to_snake, capitalize_words,
                                          chunk_list, deep_merge, flatten_dict,
                                          format_date, format_datetime,
                                          generate_id, hash_data, parse_date,
                                          sanitize_filename, snake_to_camel,
                                          truncate, unflatten_dict,
                                          unique_by_key, validate_uuid)


class TestUtilities:
    def test_generate_id(self):
        id1 = generate_id()
        id2 = generate_id()
        assert id1 != id2
        assert len(id1) == 36

    def test_format_date(self):
        date = datetime(2026, 1, 15, 10, 30, 0)
        result = format_date(date)
        assert result == "2026-01-15"

    def test_format_datetime(self):
        date = datetime(2026, 1, 15, 10, 30, 0)
        result = format_datetime(date)
        assert result == "2026-01-15 10:30:00"

    def test_parse_date(self):
        result = parse_date("2026-01-15")
        assert result is not None
        assert result.year == 2026

    def test_parse_date_invalid(self):
        result = parse_date("invalid-date")
        assert result is None

    def test_hash_data(self):
        result = hash_data("test")
        assert len(result) == 64
        assert result == hash_data("test")

    def test_validate_uuid_valid(self):
        assert validate_uuid("123e4567-e89b-12d3-a456-426614174000") is True

    def test_validate_uuid_invalid(self):
        assert validate_uuid("not-a-uuid") is False

    def test_deep_merge(self):
        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}
        result = deep_merge(base, override)
        assert result == {"a": 1, "b": {"c": 2, "d": 3}, "e": 4}

    def test_flatten_dict(self):
        d = {"a": {"b": 1, "c": 2}, "d": 3}
        result = flatten_dict(d)
        assert result == {"a.b": 1, "a.c": 2, "d": 3}

    def test_unflatten_dict(self):
        d = {"a.b": 1, "a.c": 2, "d": 3}
        result = unflatten_dict(d)
        assert result == {"a": {"b": 1, "c": 2}, "d": 3}

    def test_truncate(self):
        assert truncate("Hello World", 5) == "He..."
        assert truncate("Hi", 10) == "Hi"

    def test_capitalize_words(self):
        assert capitalize_words("hello world") == "Hello World"

    def test_snake_to_camel(self):
        assert snake_to_camel("hello_world") == "helloWorld"

    def test_camel_to_snake(self):
        assert camel_to_snake("helloWorld") == "hello_world"

    def test_sanitize_filename(self):
        assert sanitize_filename("file:name<>test.txt") == "file_name__test.txt"

    def test_chunk_list(self):
        result = chunk_list([1, 2, 3, 4, 5], 2)
        assert result == [[1, 2], [3, 4], [5]]

    def test_unique_by_key(self):
        lst = [{"id": 1, "name": "a"}, {"id": 2, "name": "b"}, {"id": 1, "name": "c"}]
        result = unique_by_key(lst, "id")
        assert len(result) == 2
