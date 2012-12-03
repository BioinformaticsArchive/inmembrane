# Program structure and APIs

The high-level structure of _inmembrane_ consists of:

- `inmembrane_scan` -- handles commandline options and calls inmembrane.process(params) to run the workflow (or runs unit tests)
- `inmembrane/__init__.py` -- a wrapper to manage configuration parameters, high-level file input and output, and execution of the specified protocol 
- `inmembrane/helpers.py` -- various helper functions that are used throughout the program
- `inmembrane/protocols` -- a module that contains protocol handlers (eg gram_pos, gram_neg). These contain the business logic of which analyses to perform (via plugins) and the rules of how to label or classify sequences based on the plugin output (eg, _if not is_signalp, label with CYTOPLASM_).
- `inmembrane/plugins` -- individual plugins for each external analysis tool. These handle the local execution (or HTTP request), parsing of output and population of labels on a sequence within the `proteins` datastructure.

### The main loop and data structure

At it's core, _inmembrane_'s task is to label ('annotate') a set of protein sequences stored within the `proteins` data structure.

The `proteins` data structure is a dictionary where the keys are the _seqid_ (sequence ID) of the protein, and the value is itself a dictionary of key-value pairs.

The program first reads a FASTA file to set up the dictionary, where at first only the 'sequence' field is created (using `helpers.create_proteins_dict()`, called from `inmembrane/__init__.py`). The `proteins` data structure is then passed to each plugin specified in the protocol, and progressively filled with properties generated by the plugin. 

Each plugin interfaces with an external analysis tool, whether through a local execution of a binary or via a web-based API.

Here is an example of a `proteins` dictionary for two sequences with _seqid_'s SPy_1392 and SPy_1379 after running a protocol to annotate them with key-value pairs (amino acid sequences shortened with '....' for clarity).

    {
    'SPy_1392': {'lipop_cleave_position': None, 'category': 'MEMBRANE(non-PSE)', 'safe_seqid': 'SPy_1392_0', 'tmhmm_inner_loops': [(1, 6), (67, 72), (126, 136), (187, 220), (281, 286), (331, 342), (395, 398)], 'tmhmm_outer_loops': [(30, 43), (94, 102), (160, 163), (244, 257), (307, 310), (366, 374)], 'name': 'SPy_1392 from AE004092', 'seq': 'MEKTKRYIIA....ALRLKK', 'hmmsearch': [], 'loop_extent': 7, 'is_signalp': False, 'details': ['tmhmm(12)'], 'sequence_length': 398, 'signalp_cleave_position': 0, 'tmhmm_helices': [(7, 29), (44, 66), (73, 93), (103, 125), (137, 159), (164, 186), (221, 243), (258, 280), (287, 306), (311, 330), (343, 365), (375, 394)], 'is_lipop': False}, 

    'SPy_1379': {'lipop_cleave_position': None, 'category': 'MEMBRANE(non-PSE)', 'safe_seqid': 'SPy_1379_1', 'tmhmm_inner_loops': [(1, 32), (82, 87), (202, 207), (268, 287), (344, 349), (405, 410)], 'tmhmm_outer_loops': [(56, 58), (106, 178), (231, 244), (307, 320), (373, 381), (434, 437)], 'name': 'SPy_1379 from AE004092', 'seq': 'MTIIIMDSNSA....FSYQFYRFILK', 'hmmsearch': [], 'loop_extent': 36, 'is_signalp': False, 'details': ['tmhmm(11)'], 'sequence_length': 437, 'signalp_cleave_position': 69, 'tmhmm_helices': [(33, 55), (59, 81), (88, 105), (179, 201), (208, 230), (245, 267), (288, 306), (321, 343), (350, 372), (382, 404), (411, 433)], 'is_lipop': False}
    }

#### Result output

The output of the program is printed to stdout in tab delimited format. Additionaly, the output is always written as a Comma Separated Values (CSV) file that can be easily imported into spreadsheet packages such as Microsoft Excel. As most users ultimately working with the output of _inmembrane_ are likely to be biologists familiar with using spreadsheets (for better or worse) for further analysis, CSV was chosen since it can be integrated into many users common workflow.

For those familiar with Python, it is relatively straightforward to modify the text output by changing `protocol.protein_output_line`, `protocol.summary_table` and `protocol.protein_csv_line` (where _protocol_ is one of the protocols in `inmembrane/protocols/*.py`).

### The protocol

One of the abstractions made in _inmembrane_ is to separate the main loop and the plugins so that _inmembrane_ can accommodate multiple workflows or 'protocols' (currently two protocols are implemented, one for Gram+ bacteria `gram_pos` and one for Gram- bacteria `gram_neg`). The choice of protocol is taken from the parameters file `inmembrane.config`. The relevant protocol is stored in a python module with the same name as the protocol in the `protocols` sub-directory.

The protocol **must** implement five functions (these are called from within `inmembrane/__init__.py`):

`get_annotations(params)` -- takes the params dictionary as input, returns a list of strings being the names of plugins to be run for this analysis (in hindsight, this function is poorly named and may be changed in the future to something like **plugins_to_run** ).

`post_process_proteins(params, proteins)` -- takes the params dictionary and the `proteins` data structure and applies any additional business logic to label sequences based on the key-value pairs already added by the plugins (eg, if is_lipop: category = "LIPOPROTEIN(non-PSE)" ).

`protein_output_line(seqid, proteins)` -- outputs annotations etc for a given seqid found in `proteins`. This is the function you should modify to change the format of results printed to stdout at the end of the analysis.

`protein_csv_line(seqid, proteins)` -- equivalent to `protein_output_line` above, but for the csv file that is written.

`summary_table(params, proteins)` -- outputs a summary table to stdout with some aggregate statistics for the entire proteome given as input.

is to add any plugins required (not all are needed, as there are many different possibilities) and send the fasta sequences, as stored in the `proteins` dictionary, into the plugin to get the desire property from that plugin.

Once all plugins have been successfully run, the plugin analyses the results of the external programs, and generates the final sub-cellular localisation and then, the 

### Parameters - load from file/and or input default

All relevant parameters for an _inmembrane_ analysis can be found in the `inmembrane.config` file, which is formatted as a Python dictionary. The dictionary is directly read in at the initialization of the program, and stored internally as `params`. The protocol and plugins all expect `params` as one of the key parameters in the main function.

### Plugins

The interface with external sequence analysis programs or web services are encapsulated within plugins. The way _inmembrane_ detects and uses plugins is straightforward: they are python modules stored in the `inmembrane/plugins` directory. The name of the module reflects the name of the program or web service and matches the naming used with `inmembrane.config`. All calls to the plugins are recognized by the module name, which can be called by `eval` within Python.

Each plugin **must** implement one function and contain one variable:

`annotate(params, proteins)` -- this takes the params dictionary and the `proteins` data structure and adds key value pairs to reflect that results of the analysis. (TODO: For convenience all plugins should return the `proteins` data structure upon successful execution, however not all plugins currently follow this rule).

`annotate` may also take other optional keyword arguments (particularly for plugins that interface with web services, it is convenient to include optional _url_ and _batchsize_ parameters, and a _force_ boolean arguments that allows cached output file to be ignored). 

`citation` -- a module level dictionary of the form:
 
`{'ref':'some citable reference', 'name':'programname version'}` (see details below).

An important element of every plugin is the parsing of the results output by the external analysis program - either text processing of an output file or stdout, handling SOAP responses (via the `suds` package) or HTML scraping of the web page output (mostly via `BeautifulSoup`). Given that Python has excellent text-processing facilities, the files are generally parsed in the main `annotate` function or an auxillary reusable function. The text files are generally sequential table-like output and so a simple iteration of the output lines is in general sufficient to process the output.

As _inmembrane_ is a glue program that builds on the work of many excellent analysis packages, _inmembrane_ takes care to make sure credit is given. As such citations for each program are considered essential parts of the plugin, and they are stored directly in the source file, and are extracted, and displayed every time the program is run and stored in `citations.txt`.

### Logging, temporary output and debugging

STDERR is used to output status messages as the program executed (eg the currently running plugin, a pseudo-progress bar if we are looping and polling a web service). These status updates should be prefixed by a # character. Most plugins etc also contain a module level variable `__DEBUG__` which prints additional information useful for debugging to STDERR. The final tab-delimited results and summary table are sent to STDOUT, so standard Unix redirection can be used to capture the two streams seperately if desired (eg `inmembrane_scan myseqs.fasta >results.out 2>results.err` )

`inmembrane` always creates a directory caching the output of external analysis packages, named based on the name of the input FASTA file without an extension. The input FASTA file is copied into this directory (as `input.fasta`), along with `citation.txt`. Output from each external package is named in the form 'plugin_name.out'.
