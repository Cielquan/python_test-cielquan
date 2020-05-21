def test_sheet_count(self, monkeypatch, mocker):
    """Test that Exception is raised when file has lees that 2 sheets."""
    monkeypatch.setattr(Path, "is_file", lambda _: True)
    monkeypatch.setattr(Path, "suffix", ".xls")
    test_wb = mocker.Mock()
    test_wb.sheetnames = []
    monkeypatch.setattr(openpyxl, "load_workbook", lambda _, data_only: test_wb)
    with pytest.raises(parser_exc.ExcelInputParserError) as exc:
        assert in_xls.extractor(excel_file="non-existing-file")
    assert "too less sheets" in str(exc)


# from pathlib import Path
# from unittest.mock import call, mock_open
#
# import pytest  # type: ignore
#
# from spotinkcalc import calc  # type: ignore
# from spotinkcalc.parser import exceptions as parser_exc  # type: ignore
# from spotinkcalc.parser import output_csv_parser as out_csv  # type: ignore


class TestParserFile:  # pylint: disable=R0201
    """Test path and naming."""

    def test_default(self, mocker, dict_spotink_percentage):
        """Test default path & file naming."""
        mocked_open = mocker.patch("builtins.open", mock_open(), create=True)
        out_csv.parser(spotink_dict=dict_spotink_percentage)
        path = Path(Path(""), "spotinks.csv")
        mocked_open.assert_called_once_with(path, "w", newline="")

    def test_custom_path(self, mocker, monkeypatch, dict_spotink_percentage):
        """Test custom path."""
        monkeypatch.setattr(Path, "is_dir", lambda _: True)
        mocked_open = mocker.patch("builtins.open", mock_open(), create=True)
        out_csv.parser(spotink_dict=dict_spotink_percentage, csv_file_path=Path("docs"))
        path = Path(Path("docs"), "spotinks.csv")
        mocked_open.assert_called_once_with(path, "w", newline="")

    def test_error_path(self, monkeypatch, dict_spotink_percentage):
        """Test erroring path."""
        monkeypatch.setattr(Path, "is_dir", lambda _: False)
        with pytest.raises(parser_exc.CSVOutputParserError) as exc:
            out_csv.parser(
                spotink_dict=dict_spotink_percentage,
                csv_file_path=Path("not-existing-dir"),
            )
        assert "Given path does not exist" in str(exc)

    def test_custom_name_wo_ending(self, mocker, dict_spotink_percentage):
        """Test custom naming w/o file ending."""
        mocked_open = mocker.patch("builtins.open", mock_open(), create=True)
        out_csv.parser(spotink_dict=dict_spotink_percentage, csv_file_name="testfile")
        path = Path(Path(""), "testfile.csv")
        mocked_open.assert_called_once_with(path, "w", newline="")

    def test_custom_name_w_ending(self, mocker, dict_spotink_percentage):
        """Test custom naming w/ file ending."""
        mocked_open = mocker.patch("builtins.open", mock_open(), create=True)
        out_csv.parser(
            spotink_dict=dict_spotink_percentage, csv_file_name="testfile.csv"
        )
        path = Path(Path(""), "testfile.csv")
        mocked_open.assert_called_once_with(path, "w", newline="")


def test_parser_content(mocker, dict_spotink_percentage):
    """Test correct writing to file."""
    mocked_open = mocker.patch("builtins.open", mock_open(), create=True)
    out_csv.parser(spotink_dict=dict_spotink_percentage)
    mocked_open.assert_called_once_with(Path(Path(""), "spotinks.csv"), "w", newline="")
    mocked_open.return_value.write.assert_has_calls(
        [
            call("SpotInk1;;\r\n"),
            call("Component;Amount;Desc\r\n"),
            call("Semi1;0.45;SemiName1\r\n"),
            call("Semi2;0.05;SemiName2\r\n"),
            call("Semi3;0.05;SemiName3\r\n"),
            call("Semi4;0.45;SemiName4\r\n"),
            call(";;\r\n"),
            call("SpotInk2;;\r\n"),
            call("Component;Amount;Desc\r\n"),
            call("Semi1;0.12;SemiName1\r\n"),
            call("Semi2;0.01;SemiName2\r\n"),
            call("Semi3;0.01;SemiName3\r\n"),
            call("Semi4;0.36;SemiName4\r\n"),
            call("RawMat1;0.5;LM\r\n"),
            call(";;\r\n"),
        ]
    )


def test_parser_content_w_sum(mocker, dict_spotink_percentage):
    """Test correct writing to file with ink '_sum'."""
    mocked_open = mocker.patch("builtins.open", mock_open(), create=True)
    dict_w_sum = calc.calc_formulation_sum(dict_spotink_percentage)
    out_csv.parser(spotink_dict=dict_w_sum)
    mocked_open.assert_called_once_with(Path(Path(""), "spotinks.csv"), "w", newline="")
    mocked_open.return_value.write.assert_has_calls(
        [
            call("SpotInk1;;\r\n"),
            call("Component;Amount;Desc\r\n"),
            call("Semi1;0.45;SemiName1\r\n"),
            call("Semi2;0.05;SemiName2\r\n"),
            call("Semi3;0.05;SemiName3\r\n"),
            call("Semi4;0.45;SemiName4\r\n"),
            call("sum;1.00;\r\n"),
            call(";;\r\n"),
            call("SpotInk2;;\r\n"),
            call("Component;Amount;Desc\r\n"),
            call("Semi1;0.12;SemiName1\r\n"),
            call("Semi2;0.01;SemiName2\r\n"),
            call("Semi3;0.01;SemiName3\r\n"),
            call("Semi4;0.36;SemiName4\r\n"),
            call("RawMat1;0.5;LM\r\n"),
            call("sum;1.00;\r\n"),
            call(";;\r\n"),
        ]
    )
