# coding=utf-8
from __future__ import unicode_literals

import unittest

from snips_nlu.intent_classifier import LogRegIntentClassifier
from snips_nlu.pipeline.configs import (
    CRFSlotFillerConfig, SlotFillerDataAugmentationConfig,
    LogRegIntentClassifierConfig, IntentClassifierDataAugmentationConfig,
    FeaturizerConfig, NLUEngineConfig, ProbabilisticIntentParserConfig,
    DeterministicIntentParserConfig)
from snips_nlu.tests.utils import SnipsTest


class TestConfig(SnipsTest):
    def test_intent_classifier_data_augmentation_config(self):
        # Given
        config_dict = {
            "min_utterances": 3,
            "noise_factor": 2,
            "unknown_word_prob": 0.1,
            "unknown_words_replacement_string": "foobar",
        }

        # When
        config = IntentClassifierDataAugmentationConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)

    def test_slot_filler_data_augmentation_config(self):
        # Given
        config_dict = {
            "min_utterances": 42,
            "capitalization_ratio": 0.66
        }

        # When
        config = SlotFillerDataAugmentationConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)

    def test_featurizer_config(self):
        # Given
        config_dict = {
            "sublinear_tf": True,
            "pvalue_threshold": 0.4,
            "word_clusters_name": None
        }

        # When
        config = FeaturizerConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)

    def test_intent_classifier_config(self):
        # Given
        config_dict = {
            "unit_name": LogRegIntentClassifier.unit_name,
            "data_augmentation_config":
                IntentClassifierDataAugmentationConfig().to_dict(),
            "featurizer_config": FeaturizerConfig().to_dict(),
            "random_seed": 42
        }

        # When
        config = LogRegIntentClassifierConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)

    def test_crf_slot_filler_config(self):
        # Given
        feature_factories = [
            {
                "args": {
                    "common_words_gazetteer_name": None,
                    "use_stemming": True,
                    "n": 1
                },
                "factory_name": "get_ngram_fn",
                "offsets": [-2, -1, 0, 1, 2]
            },
            {
                "args": {},
                "factory_name": "is_digit",
                "offsets": [-1, 0, 1]
            }
        ]
        config_dict = {
            "unit_name": "crf_slot_filler",
            "feature_factory_configs": feature_factories,
            "tagging_scheme": 2,
            "crf_args": {
                "c1": .2,
                "c2": .3,
                "algorithm": "lbfgs"
            },
            "data_augmentation_config":
                SlotFillerDataAugmentationConfig().to_dict(),
            "random_seed": 43
        }

        # When
        config = CRFSlotFillerConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)

    def test_probabilistic_intent_parser_config(self):
        # Given
        config_dict = {
            "unit_name": "probabilistic_intent_parser",
            "intent_classifier_config":
                LogRegIntentClassifierConfig().to_dict(),
            "slot_filler_config": CRFSlotFillerConfig().to_dict(),
        }

        # When
        config = ProbabilisticIntentParserConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)

    def test_deterministic_parser_config(self):
        # Given
        config_dict = {
            "unit_name": "deterministic_intent_parser",
            "max_queries": 666,
            "max_entities": 333
        }

        # When
        config = DeterministicIntentParserConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)

    def test_nlu_config_from_dict(self):
        # Given
        config_dict = {
            "unit_name": "nlu_engine",
            "intent_parsers_configs": [
                DeterministicIntentParserConfig().to_dict(),
                ProbabilisticIntentParserConfig().to_dict()
            ]
        }

        # When
        config = NLUEngineConfig.from_dict(config_dict)
        serialized_config = config.to_dict()

        # Then
        self.assertDictEqual(config_dict, serialized_config)


if __name__ == '__main__':
    unittest.main()
