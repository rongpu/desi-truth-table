Scripts that cross-match external ("truth") catalogs to Legacy Surveys sweep catalogs.

Example: cross-match DEEP2 catalogs to Legacy Surveys DR10.1 and include photo-z columns:
    
```./legacy_surveys_matching.py --ls-dr 10.1 --catalog deep2 --field south --output-dir $SCRATCH/truth/ --add-pz --plot-qa```

Here the DEEP2 parent catalogs already exist in the default location, as does the YAML file ([truth_catalogs/deep2.yaml](https://github.com/rongpu/desi-truth-table/blob/master/truth_catalogs/deep2.yaml)) containing the filenames and cross-matching parameters.

******

If you want to cross-match the Legacy Surveys to your own catalog, you need to create a YAML file and specify the `--yaml-path` and `--parent-dir` arguments, e.g.:

```./legacy_surveys_matching.py --ls-dr 10.1 --yaml-path truth_catalogs/deep2.yaml --field south --output-dir $SCRATCH/truth/ --add-pz --plot-qa --parent-dir /dvs_ro/cfs/cdirs/desi/target/analysis/truth/parent```

Note that if there are duplicates in the external catalog, only one of the duplicates will be included in the cross-matched catalog.
