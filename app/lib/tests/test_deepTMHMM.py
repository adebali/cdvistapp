import biolib
import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.dirname(__file__))
from utils import jsonFile2dict
from deepTMHMM_gff3_parser import deepTMHMM

application_name = 'DTU/DeepTMHMM:1.0.24'
app = biolib.load(application_name)
test_data_dir = os.path.join(os.path.dirname(__file__),'test-data')


@pytest.mark.parametrize(
    "input_fasta, output_dir, expected_file",
    [
        ("fasta-test.2.fa", "deepTMHMM_test_results", "deepTMHMM_gff3_results.json"),
        ("fasta-test.3.fa", "deepTMHMM_test_results_3", "deepTMHMM_gff3_results_3.json"),
    ]
)


def test_deepTMHMM(input_fasta, output_dir, expected_file, request):
    # Check if the --run-long option is provided
    if request.config.getoption("--run-long"):
          
        # Run the longer test process
        input_file = os.path.join(test_data_dir, input_fasta)
        result = app.cli(args=f'--fasta {input_file}', machine='local')
        result.save_files(os.path.join(test_data_dir, output_dir))

    # Perform assertions
    output_file= os.path.join(test_data_dir, output_dir, 'TMRs.gff3')
    deepTMHMMobject = deepTMHMM(output_file)
    sorted_deepTMHMMobject = sorted(deepTMHMMobject.results, key=lambda x: x["protein"])
    expectedDomains = jsonFile2dict(os.path.join(test_data_dir, expected_file))
    sorted_expectedDomains = sorted(expectedDomains, key=lambda x: x["protein"])
    assert sorted_deepTMHMMobject == sorted_expectedDomains, f"Expected: {sorted_expectedDomains}, but got: {sorted_deepTMHMMobject}"

# test_deepTMHMM("fasta-test.3.fa", "deepTMHMM_test_results_3", "deepTMHMM_gff3_results_3.json")