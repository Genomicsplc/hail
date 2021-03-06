
from __future__ import absolute_import
from hail.history import *
from hail.typecheck import *
from hail.utils.java import *


class KinshipMatrix(HistoryMixin):
    """
    Represents a symmetric matrix encoding the relatedness of each pair of samples in the accompanying sample list.
    
    The output formats are consistent with `PLINK formats <https://www.cog-genomics.org/plink2/formats>`_ as created by the `make-rel and make-grm commands <https://www.cog-genomics.org/plink2/distance#make_rel>`_ and used by `GCTA <http://cnsgenomics.com/software/gcta/estimate_grm.html>`_.

    """
    def __init__(self, jkm):
        self._key_schema = None
        self._jkm = jkm

    @classmethod
    @record_classmethod
    def _from_block_matrix(cls, sample_schema, bm, sample_ids, n_variants):
        return cls(Env.hail().methods.KinshipMatrix.apply(
            Env.hc()._jhc,
            sample_schema._jtype,
            bm._jbm,
            sample_ids,
            n_variants))

    @property
    @handle_py4j
    def key_schema(self):
        """
        Returns the signature of the key indexing this matrix.

        :rtype: :class:`.Type`
        """
        from hail.expr import Type
        if self._key_schema is None:
            self._key_schema = Type._from_java(self._jkm.sampleSignature())
        return self._key_schema

    @handle_py4j
    def sample_list(self):
        """
        Gets the list of samples. The (i, j) entry of the matrix encodes the relatedness of the ith and jth samples.

        :return: List of samples.
        :rtype: list of str
        """
        return [self.key_schema._convert_to_py(s) for s in self._jkm.sampleIds()]

    @handle_py4j
    def matrix(self):
        """
        Gets the matrix backing this kinship matrix.

        :return: MatrixTable of kinship values.
        :rtype: `IndexedRowMatrix <https://spark.apache.org/docs/latest/api/python/pyspark.mllib.html#pyspark.mllib.linalg.distributed.IndexedRowMatrix>`__
        """
        from pyspark.mllib.linalg.distributed import IndexedRowMatrix

        return IndexedRowMatrix(self._jkm.matrix())

    @handle_py4j
    @typecheck_method(output=strlike)
    @write_history('output')
    def export_tsv(self, output):
        """
        Export kinship matrix to tab-delimited text file with sample list as header.

        **Notes**

        A text file containing the python code to generate this output file is available at ``<output>.history.txt``.
        
        :param str output: File path for output. 
        """
        self._jkm.exportTSV(output)

    @handle_py4j
    @typecheck_method(output=strlike)
    @write_history('output')
    def export_rel(self, output):
        """
        Export kinship matrix as .rel file. See `PLINK formats <https://www.cog-genomics.org/plink2/formats>`_.

        **Notes**

        A text file containing the python code to generate this output file is available at ``<output>.history.txt``.

        :param str output: File path for output. 
        """
        self._jkm.exportRel(output)

    @handle_py4j
    @typecheck_method(output=strlike)
    @write_history('output')
    def export_gcta_grm(self, output):
        """
        Export kinship matrix as .grm file. See `PLINK formats <https://www.cog-genomics.org/plink2/formats>`_.

        **Notes**

        A text file containing the python code to generate this output file is available at ``<output>.history.txt``.

        :param str output: File path for output.
        """
        self._jkm.exportGctaGrm(output)

    @handle_py4j
    @typecheck_method(output=strlike,
                      opt_n_file=nullable(strlike))
    @write_history('output')
    def export_gcta_grm_bin(self, output, opt_n_file=None):
        """
        Export kinship matrix as .grm.bin file or as .grm.N.bin file, depending on whether an N file is specified. See `PLINK formats <https://www.cog-genomics.org/plink2/formats>`_.

        **Notes**

        A text file containing the python code to generate this output file is available at ``<output>.history.txt``.

        :param str output: File path for output. 
        
        :param opt_n_file: The file path to the N file. 
        :type opt_n_file: str or None
        """
        self._jkm.exportGctaGrmBin(output, joption(opt_n_file))

    @handle_py4j
    @typecheck_method(output=strlike)
    @write_history('output')
    def export_id_file(self, output):
        """
        Export samples as .id file. See `PLINK formats <https://www.cog-genomics.org/plink2/formats>`_.

        **Notes**

        A text file containing the python code to generate this output file is available at ``<output>.history.txt``.

        :param str output: File path for output.
        """
        self._jkm.exportIdFile(output)
