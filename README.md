# JAK-gb

A collection of tools to merge, summarize and update genbank record annotations.

# Summarize a Genbank file

The `genbankSummary.py` file will return a list of features and qualifiers for each record in a genbank file.

```
usage: genbankSummary.py [-h] -g GENBANK [-i ID]

Summarize the contents of a genbank file or record

optional arguments:
  -h, --help            show this help message and exit
  -g GENBANK, --genbank GENBANK
                        Genbank file to summarize
  -i ID, --id ID        Limit to only the record with this ID
```

## Options

### genbank (g)

`required`

For the path to the `.gb` file. This can either be a single record, or multiple genbank records concatenated together. The summary will be reported for each record independently if it is a multi-genbank file.

### id (i)

`default = all`

For the ID of a genbank record if you only want to report one record within a multi-genbank file.

## Output

### Feature Types

This is just a count of feature types within the record.

Currently, the feature types are limited to only `CDS`, `rRNA` and `tRNA` types, but this can be edited in the script in the `featureTypePrint` list.

### Qualifier Types

This is a count of all of the qualifier types within the features. Many features have overlapping qualifiers, for example, the same `locus_tag` is found the `CDS`, `gene` and `misc_features` feature types, and probably many more. In parentheses is the non-redundant count for these features within the record.

The qualifiers displayed is also limited to those within the `qualifierTypePrint` list, and can be modified to show other types if necessary. It currently only shows `locus_tag`, `db_xref`, `translation`, `EC_number` and `product`.

### db_xref Types

Since `db_xref` is the catch-all for different types of annotations, they are all listed out here. Each `db_xref` record has a `TYPE:VALUE` format, and these are summarized for total counts, as well as for unique values (two CDSs with the same `TYPE:VALUE`).

# Merge Two Genbanks Files

The `mergeGenbank.py` script takes a “secondary” genbank file, and merges its qualifiers into a “master” genbank file. It currently finds similar CDS features between the two genbank files solely on `source` length and `feature` position. This is because genbank files generated from some sources (such as RAST) often remove all CDS identifiers such as `locus_tag` or `protein_id`, and only location information is preserved.

```
usage: mergeGenbank.py [-h] -m MASTER -s SECONDARY [-f FOLDER]

Merge CDS qualifiers of a secondary (-s) Genbank file into a Master (-m)

optional arguments:
  -h, --help            show this help message and exit
  -m MASTER, --master MASTER
                        Master genbank file
  -s SECONDARY, --secondary SECONDARY
                        Genbank file to merge into master
  -f FOLDER, --folder FOLDER
                        Output folder, defaults to mergedOutput + timestamp
```

## Options

### master (m)

`required`

The “master” genbank file. Nothing will be removed from this record, and it will act as a backbone for adding additional annotations.

### secondary (s)

`required`

The “secondary” genbank file. Qualifiers from this record will be moved to the “master”.

### folder (f)

`default = mergedOutput_timestamp`

The output folder that the records will be saved to.

## Output
This script will save all records as their own `.gbk` file. To merge into a single concatenated record called `merged.gbk`,, from the command line type

```
cat *.gbk > merged.gbk`
```

# Add Annotations to a Genbank File

The `updateGenbankAnnotations.py` script will take a tab-delimited file of annotations, and add or overwrite a genbank file.

```
usage: updateGenbankAnnotations.py [-h] -g GENBANK -a ANNOTATIONS [-m METHOD]
                                   [-i IDENTIFIER] [-q QUALIFIER]
                                   [-x DB_XREF_TYPE] [-f FOLDER]

Add or overwrite annotations in a genbank file

optional arguments:
  -h, --help            show this help message and exit
  -g GENBANK, --genbank GENBANK
                        Genbank file to update
  -a ANNOTATIONS, --annotations ANNOTATIONS
                        File with annotations (col1=identifier, col2=new
                        annotation)
  -m METHOD, --method METHOD
                        'o'=overwite, 'a'=append/add
  -i IDENTIFIER, --identifier IDENTIFIER
                        Type of annotation from column 1 of annotations file
                        (ex. 'locus_tag', 'GI') to look for in the genbank
                        file
  -q QUALIFIER, --qualifier QUALIFIER
                        Qualifier to add new annotations to (ex. 'product',
                        'db_xref')
  -x DB_XREF_TYPE, --db_xref_type DB_XREF_TYPE
                        If using -q db_xref this option will prepend
                        annotations with this variable, if your annotations
                        file is missing it (ex. 'GO', 'SEED')
  -f FOLDER, --folder FOLDER
                        Output folder, defaults to updatedOutput + timestamp
```

## Options

### genbank (g)

`required`

The filepath of the genbank file.

### annotations (a)

`required`

The filepath to the annotations file. This should be a 2-column, tab-delimited file with the `identifier` in column 1, and the annotation in column 2.

### method (m)

`default = a`

The method for updating. If set to “o”, it will overwrite the qualifier in the genbank file. If set to “a”, it will add or append to the genbank file.

### identifier (i)

`default = locus_tag`

Due to their being different ways to map a feature in the genbank file with the feature in the annotations file, the script uses an `identifier` to map between the two files. For example, if your both your genbank and annotations file use `locus_tag`, then ‘locus_tag’ would be the identifier.

### qualifier (q)

`default = product`

The `qualifier` that you want column 2 to be mapped to. For example, the default is `product`, so after identifying the correct genbank entry based on the `identifier`, the `product` will be updated with the annotation in column 2.

### db_xref (x)

`default = none`

If `-q` is `db_xref`, this option can add an additional prefix to the beginning of the annotations. For example, suppose you had the following annotations file of `locus_tag` and `GO` terms:

```
Gal_00002	0003887
Gal_00007	0003918
Gal_00019	0003677
```

Use the flags `-i locus_tag` to match the locus_tags between records, `-q db_xref` to add the column 2 annotations to a db_xref qualifier, and `-x GO` to prefix annotations with `GO:` (no need to add the “:”). This will add the following lines to the appropriate locus tags in the genbank file:

```
/db_xref="GO:0003887”
/db_xref="GO:0003918”
/db_xref="GO:0003677”
```

This can also be used for custom annotation types, such as `signalP`, `transporter`, or anything else you may want to add.

### folder (f)

`default=updatedOutput_timestamp`

This is the output folder that the new genbank files will be written to.

## Output

New genbank files, one for each record. See above for concatenation code.
