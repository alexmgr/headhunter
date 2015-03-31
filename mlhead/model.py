# -*- coding:utf-8 -*-

import os

class CorpusError(Exception):
  pass

class CorpusFolder(object):
  TRAIN = "train"
  TEST = "test"

class Corpus(object):

  subdirs = set((CorpusFolder.TRAIN, CorpusFolder.TEST))
  
  def __init__(self, folder):
    if self._valid_corpus_struct(folder):
      self.root = os.path.abspath(folder)
      self.train = os.path.join(self.root, CorpusFolder.TRAIN)
      self.test = os.path.join(self.root, CorpusFolder.TEST)

  def _valid_corpus_struct(self, folder):
    if not os.path.isdir(folder):
      raise CorpusError("Unable to access corpus directory: %s" % folder)
    if not len(set(os.listdir(folder)).intersection(Corpus.subdirs)) == len(Corpus.subdirs):
      raise CorpusError("Corpus directory missing subfolders. Expecting: %s" % Corpus.subdirs)
    else:
      return True

  def training_pcaps(self, subdir=None):
    pass

if __name__ == "__main__":
  import shutil
  import tempfile
  import unittest

  class TestCorpus(unittest.TestCase):

    def setUp(self):
      self.root = tempfile.mkdtemp()
      self.train = os.path.join(self.root, CorpusFolder.TRAIN)
      self.test = os.path.join(self.root, CorpusFolder.TEST)
      os.makedirs(self.train)
      os.makedirs(self.test)

    def tearDown(self):
      shutil.rmtree(self.root)

    def test_invalid_root_folder_should_raise_error(self):
      file_ = tempfile.mktemp()
      with self.assertRaises(CorpusError):
        Corpus(file_)

    def test_missing_training_folder_raises_error(self):
      shutil.rmtree(self.train)
      with self.assertRaises(CorpusError):
        Corpus(self.root)

    def test_missing_test_folder_raises_error(self):
      shutil.rmtree(self.test)
      with self.assertRaises(CorpusError):
        Corpus(self.root)

    def test_additional_folder_under_root_has_no_effect(self):
      os.makedirs(os.path.join(self.root, "other_folder"))
      corpus = Corpus(self.root)
      self.assertTrue(corpus is not None)

    def test_corpus_is_built_on_valid_struct(self):
      corpus = Corpus(self.root)
      self.assertEqual(corpus.root, self.root)
      self.assertEqual(corpus.train, self.train)
      self.assertEqual(corpus.test, self.test)

  unittest.main()
