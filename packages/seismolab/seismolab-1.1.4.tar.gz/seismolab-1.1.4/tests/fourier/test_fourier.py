import pytest
from numpy.testing import assert_array_almost_equal
import numpy as np

from seismolab.fourier import Fourier, MultiHarmonicFitter, MultiFrequencyFitter

@pytest.fixture
def light_curve():
    time,brightness = np.loadtxt('st_pic_light_curve.txt',unpack=True)
    return time,brightness

@pytest.fixture
def spectrum():
    FFf, FFp = np.loadtxt('st_pic_spectrum.txt',unpack=True)
    return FFf, FFp

@pytest.fixture
def spectral_window():
    swf,swp = np.loadtxt('st_pic_spectral_window.txt',unpack=True)
    return swf,swp

def test_Fourier(light_curve,spectrum,spectral_window):
    time,brightness = light_curve

    FF = Fourier(time,brightness)
    FFf, FFp = FF.spectrum()
    swf,swp  = FF.spectral_window()

    FFf_in, FFp_in = spectrum
    swf_in, swp_in = spectral_window

    assert_array_almost_equal(FFf,FFf_in)
    assert_array_almost_equal(FFp,FFp_in)

    assert_array_almost_equal(swf,swf_in)
    assert_array_almost_equal(swp,swp_in)

@pytest.fixture
def pfit_perr():
    pfit,perr = np.loadtxt('st_pic_pfit_perr.txt',unpack=True)
    return pfit,perr

@pytest.fixture
def load_lcmodel():
    lcmodel = np.loadtxt('st_pic_lcmodel.txt',unpack=True)
    return lcmodel

def test_MultiHarmonicFitter(light_curve,pfit_perr,load_lcmodel):
    time,brightness = light_curve

    fitter = MultiHarmonicFitter(time,brightness)
    pfit,perr = fitter.fit_harmonics()
    tmodel = np.linspace(time.min(),time.max(),10000)
    lcmodel = fitter.lc_model(tmodel,*pfit)

    pfit_in, perr_in = pfit_perr
    lcmodel_in = load_lcmodel

    ncomponents = int((len(pfit)-1)/2)

    # Check frequency + amplitudes
    assert_array_almost_equal(pfit[:1+ncomponents],pfit_in[:1+ncomponents])
    # Check zero point
    assert_array_almost_equal(pfit[-1],pfit_in[-1])
    # Check phases
    assert_array_almost_equal(pfit[1+ncomponents:-1],pfit_in[1+ncomponents:-1],decimal=3)
    # Check errors
    assert_array_almost_equal(perr,perr_in)
    # Check light curve model
    assert_array_almost_equal(lcmodel,lcmodel_in)

@pytest.fixture
def pfit_perr_all():
    pfit,perr = np.loadtxt('st_pic_pfit_perr_all.txt',unpack=True)
    return pfit,perr

def test_MultiFrequencyFitter(light_curve,pfit_perr_all):
    time,brightness = light_curve

    fitter = MultiFrequencyFitter(time,brightness)
    pfit,perr = fitter.fit_freqs()

    pfit_in, perr_in = pfit_perr_all

    ncomponents = int((len(pfit)-1)//3)

    # Check frequency
    assert_array_almost_equal(pfit[:ncomponents],pfit_in[:ncomponents])
    # Check amplitudes
    assert_array_almost_equal(pfit[ncomponents:2*ncomponents],pfit_in[ncomponents:2*ncomponents])
    # Check zero point
    assert_array_almost_equal(pfit[-1],pfit_in[-1])
    # Check phases
    assert_array_almost_equal(pfit[2*ncomponents:-1],pfit_in[2*ncomponents:-1],decimal=3)

