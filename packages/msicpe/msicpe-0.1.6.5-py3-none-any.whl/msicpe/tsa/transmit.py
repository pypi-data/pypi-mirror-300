import numpy as np

def _noise_psd(N, iden,powB, psd = lambda f: 1):
        B= np.zeros(N)
        match iden:
            case 1:
                B = np.sqrt(powB)*np.random.randn(N)
            case 2:
                B = np.random.uniform(-np.sqrt(3*powB),np.sqrt(3*powB),N)
            case 3:
                # B = np.random.poisson(powB,N)
                B = np.random.exponential(1/powB,N)
        X_white = np.fft.rfft(B)
        S = psd(np.fft.rfftfreq(N))
        # Normalize S -> makes sure that the colored noise will preserve the energy of the white noise.
        S = S / np.sqrt(np.mean(S**2))
        X_shaped = X_white * S
        return np.fft.irfft(X_shaped)

def _PSDGenerator(f):
    return lambda N,iden,powB: _noise_psd(N,iden,powB,f)

@_PSDGenerator
def _white_noise(f):
    return 1

@_PSDGenerator
def _blue_noise(f):
    return np.sqrt(f)

@_PSDGenerator
def _violet_noise(f):
    return f

@_PSDGenerator
def _brownian_noise(f):
    return 1/np.where(f == 0, float('inf'), f)

@_PSDGenerator
def _pink_noise(f):
    return 1/np.where(f == 0, float('inf'), np.sqrt(f))

def transmit(S, canal_id: int, powB=1):
    """
    TRANSMIT modélise un canal de transmission bruité.

    Parameters
    ----------
    S : array_like
        signal à transmettre
        
    canal_id : int
        identifiant du canal de transmission (entre 0 et 15)
        
    powB :float, optional
        puissance du bruit de transmission (valeur par défaut: 1)

    Returns
    -------
    X : ndarray
        signal dégradé après transmission
    """
    
    B= np.zeros(S.size)
    if 0<canal_id<4:
        B= _white_noise(S.size,canal_id,powB)
    elif 4<= canal_id<7:
        B= _pink_noise(S.size,canal_id-3,powB)
    elif 7<= canal_id<10:
        B= _blue_noise(S.size,canal_id-6,powB)
    elif 10<= canal_id<13:
        B= _violet_noise(S.size,canal_id-9,powB)
    elif 13<= canal_id<16:
        B= _brownian_noise(S.size,canal_id-12,powB)
    elif canal_id<0 or canal_id<=16:
        ValueError('numero de canal incorrect, merci d''entrer une valeur entre 0 et 15')
    
    B=np.reshape(B,*S.shape)    
    X = S + B
    return X

def transmit_old(S, powB=5):
    """
    TRANSMIT modélise un canal de transmission bruité.

    Parameters
    ----------
    S : array_like
        signal à transmettre
    powB :float, optional
        puissance du bruit de transmission (valeur par défaut: 5)

    Returns
    -------
    X : ndarray
        signal dégradé après transmission
    B : ndarray
        bruit introduit par le canal de transmission
    """
    B = np.sqrt(powB) * np.random.randn(*S.shape)
    X = S + B
    return X, B

#
# # Exemple d'utilisation
# import plotly.graph_objs as go
# import plotly.io as pio
#
# # Signal d'exemple
# S = np.sin(2 * np.pi * np.linspace(0, 1, 1000))  # Signal sinusoïdal
#
# # Transmettre le signal avec bruit
# X, B = transmit(S)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=np.arange(len(S)), y=S, mode='lines', name='Signal original'))
# fig.add_trace(go.Scatter(x=np.arange(len(X)), y=X, mode='lines', name='Signal transmis'))
# fig.add_trace(go.Scatter(x=np.arange(len(B)), y=B, mode='lines', name='Bruit'))
#
# fig.update_layout(title='Transmission de Signal avec Bruit',
#                   xaxis_title='Temps',
#                   yaxis_title='Amplitude')
#
# pio.show(fig)
# # Exemple d'utilisation
# import plotly.graph_objs as go
# import plotly.io as pio
#
# # Signal d'exemple
# S = np.sin(2 * np.pi * np.linspace(0, 1, 1000))  # Signal sinusoïdal
#
# # Transmettre le signal avec bruit
# X, B = transmit(S)
#
# # Affichage des résultats avec Plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=np.arange(len(S)), y=S, mode='lines', name='Signal original'))
# fig.add_trace(go.Scatter(x=np.arange(len(X)), y=X, mode='lines', name='Signal transmis'))
# fig.add_trace(go.Scatter(x=np.arange(len(B)), y=B, mode='lines', name='Bruit'))
#
# fig.update_layout(title='Transmission de Signal avec Bruit',
#                   xaxis_title='Temps',
#                   yaxis_title='Amplitude')
#
# pio.show(fig)