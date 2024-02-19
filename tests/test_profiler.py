import pytest
from _pstats import PStatsSerializer
from profiler import Profiler


class DummuStringPStatsSerializer(PStatsSerializer):
    def serialize(self):
        return "Some serialized data"


def func_for_profiling():
    return True


class TestProfiler:
    def test_profiling_result_as_string(self, mocker, with_fake_profile_runcall):
        mocker.patch("profiler.PStats", return_value=mocker.Mock())

        profiler = Profiler()
        retval = profiler.profile(func_for_profiling)
        profiling_result = profiler.serialize_result(
            serializer=DummuStringPStatsSerializer, stack_size=10
        )

        assert retval is True
        assert profiling_result == "Some serialized data"
