from vardiff import FileDiff
import tempfile

def test_compare_identical_files():
    file1 = tempfile.NamedTemporaryFile(delete=False)
    file2 = tempfile.NamedTemporaryFile(delete=False)

    try:
        file1.write(b"Line 1\nLine 2\nLine 3\n")
        file2.write(b"Line 1\nLine 2\nLine 3\n")
        file1.close()
        file2.close()

        fc = FileDiff()
        assert fc.compare_files(file1.name, file2.name) == True

    finally:
        file1.close()
        file2.close()

def test_compare_different_files():
    file1 = tempfile.NamedTemporaryFile(delete=False)
    file2 = tempfile.NamedTemporaryFile(delete=False)

    try:
        file1.write(b"Line 1\nLine 2\nLine 3\n")
        file2.write(b"Line 1\nLine 2\nDifferent line\n")
        file1.close()
        file2.close()

        fc = FileDiff()
        result = fc.compare_files(file1.name, file2.name)
        assert "file_differences" in result

    finally:
        file1.close()
        file2.close()
