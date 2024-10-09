import numpy as np


def TransFourier2(s, t=None, fmax=None):
    """
    Calcul de la transformée de Fourier d'un signal s sur un intervalle de fréquences spécifié.

    Parameters
    ----------
    s : array_like
        Vecteur de taille N contenant les N échantillons s[n] du signal à analyser.
    t : array_like, optional
        Vecteur de taille N contenant les instants d'échantillonnage de s.
        Par défaut, t = [0, 1, 2, ..., N-1].
    fmax : float, optional
        Fréquence maximale pour la transformée de Fourier. Peut être supérieure à Fe/2.

    Returns
    -------
    S : numpy.ndarray
        Vecteur de taille N contenant les coefficients de la transformée de Fourier du signal s sur l'intervalle spécifié.
    f : numpy.ndarray
        Vecteur de taille N contenant les fréquences correspondant aux coefficients de S : S[n] = S(f[n]).

    Raises
    ------
    ValueError
        Si les vecteurs `s` et `t` n'ont pas la même longueur.
        Si `t` n'est pas linéairement croissant avec un pas constant.
    """
    S, f = trans_fourier(s, t)

    if fmax is not None:
        Fe = 1.0 / (t[1] - t[0]) if t is not None else 1.0
        M = len(S)
        df = Fe / M
        f_new = np.arange(-fmax, fmax, df)

        # Ajuster f_new pour qu'il soit dans l'intervalle [-Fe/2, Fe/2]
        f2 = np.mod(f_new + Fe/2, Fe) - Fe/2

        # Calculer les indices correspondants
        indices = np.round(f2 / df).astype(int)
        indices = np.mod(indices, M)  # Assurer que les indices sont dans [0, M-1]

        S_new = S[indices]
        f_new = f_new[:len(S_new)]  # Ajuster la taille si nécessaire

        return S_new, f_new

    return S, f