# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Leland Stanford Junior University
# Copyright (c) 2018 The Regents of the University of California
#
# This file is part of pelicun.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# You should have received a copy of the BSD 3-Clause License along with
# pelicun. If not, see <http://www.opensource.org/licenses/>.
#
# Contributors:
# Adam Zsarnóczay
# John Vouvakis Manousakis

"""
These are unit and integration tests on the assessment module of pelicun.
"""

import pytest
from pelicun import base
from pelicun import model
from pelicun import assessment

# pylint: disable=missing-function-docstring


def create_assessment_obj(config=None):
    if config:
        asmt = assessment.Assessment(config)
    else:
        asmt = assessment.Assessment({})
    return asmt


def test_Assessment_init():
    asmt = create_assessment_obj()

    assert asmt.stories is None

    assert asmt.options
    assert isinstance(asmt.options, base.Options)

    assert asmt.unit_conversion_factors
    assert isinstance(asmt.unit_conversion_factors, dict)

    assert asmt.log
    assert isinstance(asmt.log, base.Logger)

    # test attributes defined as properties
    assert asmt.demand
    assert isinstance(asmt.demand, model.DemandModel)
    assert asmt.asset
    assert isinstance(asmt.asset, model.AssetModel)
    assert asmt.damage
    assert isinstance(asmt.damage, model.DamageModel)
    assert asmt.repair
    assert isinstance(asmt.repair, model.RepairModel)


def test_assessment_get_default_metadata():
    asmt = create_assessment_obj()

    data_sources = (
        'damage_DB_FEMA_P58_2nd',
        'damage_DB_Hazus_EQ_bldg',
        'damage_DB_Hazus_EQ_trnsp',
        'loss_repair_DB_FEMA_P58_2nd',
        'loss_repair_DB_Hazus_EQ_bldg',
        'loss_repair_DB_Hazus_EQ_trnsp',
    )

    for data_source in data_sources:
        # here we just test that we can load the data file, without
        # checking the contens.
        asmt.get_default_data(data_source)
        asmt.get_default_metadata(data_source)


def test_assessment_calc_unit_scale_factor():
    # default unit file
    asmt = create_assessment_obj()

    # without specifying a quantity
    assert asmt.calc_unit_scale_factor('m') == 1.00
    assert asmt.calc_unit_scale_factor('in') == 0.0254

    # with quantity
    assert asmt.calc_unit_scale_factor('2.00 m') == 2.00
    assert asmt.calc_unit_scale_factor('2 in') == 2.00 * 0.0254

    # when a custom unit file is specified, changing the base units
    asmt = create_assessment_obj(
        {
            'UnitsFile': (
                'pelicun/tests/data/assessment/'
                'test_assessment_calc_unit_scale_factor/'
                'custom_units.json'
            )
        }
    )

    assert asmt.calc_unit_scale_factor('in') == 1.00
    assert asmt.calc_unit_scale_factor('m') == 39.3701

    # exceptions

    # unrecognized unit
    with pytest.raises(KeyError):
        asmt.calc_unit_scale_factor('smoot')
        # 1 smoot was 67 inches in 1958.


def test_assessment_scale_factor():
    # default unit file
    asmt = create_assessment_obj()
    assert asmt.scale_factor('m') == 1.00
    assert asmt.scale_factor('in') == 0.0254

    # when a custom unit file is specified, changing the base units
    asmt = create_assessment_obj(
        {
            'UnitsFile': (
                'pelicun/tests/data/assessment/'
                'test_assessment_calc_unit_scale_factor/'
                'custom_units.json'
            )
        }
    )

    assert asmt.scale_factor('in') == 1.00
    assert asmt.scale_factor('m') == 39.3701

    # exceptions
    with pytest.raises(ValueError):
        asmt.scale_factor('helen')
