import pandas as pd
from .testers import StationarityTester
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
from sklearn.preprocessing import StandardScaler

class Returns_Calculator(BaseEstimator, TransformerMixin, StationarityTester):
    """
    Esta clase calcula los retornos porcentuales de un conjunto de características, dependiendo de si las 
    características pasan la prueba de estacionariedad.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.
    StationarityTester : Clase personalizada que contiene una función para evaluar la estacionariedad.

    Atributos:
    ----------
    threshold : float
        Umbral para determinar si una característica es estacionaria.
    
    period : int
        Período para el cálculo de los retornos porcentuales (n períodos previos).

    Métodos:
    --------
    __init__(threshold, period):
        Inicializa la clase con un umbral para la estacionariedad y un período para calcular los retornos.
    
    fit(X, y=None):
        Evalúa la estacionariedad de las características en X, almacena las columnas y los índices, 
        y calcula los valores eliminados para la inversa.
    
    transform(X, y=None):
        Aplica el cálculo de retornos a las características que no son estacionarias.
    
    inverse_transform(X, y=None):
        Restaura los valores originales, deshaciendo la transformación de los retornos porcentuales.
    """

    def __init__(self, threshold, period):
        """
        Inicializa la clase Returns_Calculator con el umbral para la estacionariedad y el período para los retornos.

        Parámetros:
        -----------
        threshold : float
            El umbral para determinar si una característica es estacionaria.
        
        period : int
            El período que se utilizará para calcular los retornos porcentuales.
        """
        self.threshold = threshold
        self.period = period

    def fit(self, X, y=None):
        """
        Ajusta el transformador evaluando la estacionariedad de cada característica y almacena información
        sobre las columnas e índices de los datos.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre las cuales se evaluará la estacionariedad.

        y : None
            No utilizado.

        Retorna:
        --------
        self : Returns_Calculator
            El propio objeto para permitir el encadenamiento.
        """
        self.columns = X.columns
        self.index = X.index
        self.evaluations = {}
        for feature in X:
            evaluation = self.evaluate(X[feature])
            self.evaluations[feature] = evaluation
        self.deleted_values = X.iloc[:self.period, :].copy()
        return self

    def transform(self, X, y=None):
        """
        Transforma los datos aplicando el cálculo de retornos a las características no estacionarias.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre el cual se aplicará la transformación.

        y : None
            No utilizado.

        Retorna:
        --------
        transformed_X : DataFrame
            Los datos transformados, sin las primeras 'period' filas.
        """
        transformed_X = X.copy()
        for feature, condition in self.evaluations.items():
            if condition:
                transformed_X[feature] = transformed_X[feature].pct_change(periods=self.period)
        transformed_X = transformed_X.iloc[self.period:, :]
        return transformed_X

    def inverse_transform(self, X, y=None):
        """
        Deshace la transformación de los retornos porcentuales, restaurando los valores originales.

        Parámetros:
        -----------
        X : DataFrame
            Los datos transformados de los cuales se quieren recuperar los valores originales.

        y : None
            No utilizado.

        Retorna:
        --------
        restored_df : DataFrame
            Los datos restaurados a su forma original antes de la transformación.
        """
        restored_df = pd.concat([self.deleted_values, X], axis=0)
        restored_df.columns = self.columns
        restored_df.index = self.index
        for idx in range(restored_df.shape[1]):
            if not self.evaluations[self.columns[idx]]:
                continue
            unstructured_values = restored_df.iloc[:, idx].values
            reestructured_values = []
            for value_idx, current_value in enumerate(unstructured_values):
                if value_idx < self.period:
                    reestructured_values.append(current_value)
                else:
                    reestructured_values.append(reestructured_values[value_idx - self.period] * (1 + unstructured_values[value_idx]))
            restored_df.iloc[:, idx] = reestructured_values
        return restored_df


class Stationater(BaseEstimator, TransformerMixin, StationarityTester):
    """
    Esta clase aplica diferencias a las características para convertirlas en estacionarias, 
    hasta un límite máximo de diferenciación.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.
    StationarityTester : Clase personalizada que contiene una función para evaluar la estacionariedad.

    Atributos:
    ----------
    threshold : float
        Umbral para determinar si una característica es estacionaria.
    
    diff_limit : int
        Límite máximo de diferenciaciones permitidas para lograr estacionariedad.

    Métodos:
    --------
    __init__(threshold, diff_limit):
        Inicializa la clase con el umbral para la estacionariedad y el límite máximo de diferenciaciones.
    
    fit(X, y=None):
        Evalúa la estacionariedad de las características y calcula el número de diferenciaciones necesarias para cada una.
    
    transform(X, y=None):
        Aplica las diferenciaciones necesarias a las características para hacerlas estacionarias.
    
    inverse_transform(X, y=None):
        Deshace las diferenciaciones aplicadas, restaurando los valores originales.
    """

    def __init__(self, threshold, diff_limit):
        """
        Inicializa la clase Stationater con un umbral para la estacionariedad y un límite de diferenciación.

        Parámetros:
        -----------
        threshold : float
            El umbral para determinar si una característica es estacionaria.
        
        diff_limit : int
            El límite máximo de diferenciaciones permitidas para una característica.
        """
        self.threshold = threshold
        self.diff_limit = diff_limit

    def fit(self, X, y=None):
        """
        Ajusta el transformador evaluando la estacionariedad de cada característica y determina cuántas 
        diferenciaciones se necesitan para cada una.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre las cuales se evaluará la estacionariedad.

        y : None
            No utilizado.

        Retorna:
        --------
        self : Stationater
            El propio objeto para permitir el encadenamiento.
        """
        self.columns = X.columns
        self.index = X.index
        self.orders_diff = {}
        for feature in range(X.shape[1]):
            feature_diff_orders = 0
            X_for_test = X.copy()
            contador = 0
            while True:
                evaluation = self.evaluate(X_for_test.iloc[:, feature])
                if not evaluation:
                    break
                if contador == self.diff_limit:
                    print(f'diff limit reached by {feature}')
                    break
                feature_diff_orders += 1
                X_for_test = pd.DataFrame(np.diff(X_for_test, axis=0))
                contador += 1
            self.orders_diff[feature] = feature_diff_orders
        return self

    def transform(self, X, y=None):
        """
        Transforma los datos aplicando diferenciaciones a las características que no son estacionarias.

        Parámetros:
        -----------
        X : DataFrame
            El conjunto de características sobre el cual se aplicará la transformación.

        y : None
            No utilizado.

        Retorna:
        --------
        new_df : DataFrame
            Los datos transformados con diferenciaciones aplicadas para hacerlos estacionarios.
        """
        new_columns = []
        self.deleted_values = {}
        for feature, order_diff in self.orders_diff.items():
            feature_deleted_values = []
            new_column = X.iloc[:, feature].values
            if order_diff == 0:
                new_columns.append(new_column)
            else:
                for order in range(order_diff):
                    feature_deleted_values.append(new_column[0])
                    new_column = np.diff(new_column)
                new_columns.append(new_column)
            self.deleted_values[feature] = feature_deleted_values

        largest_shape = max(len(arr) for arr in new_columns)
        for feature, array in enumerate(new_columns):
            if array.dtype == 'int64':
                array = array.astype('float64')
            while array.shape[0] != largest_shape:
                array = np.insert(array, 0, np.nan)
            new_columns[feature] = array

        new_df = pd.DataFrame(new_columns).T
        new_df.columns = self.columns

        for idx in range(new_df.shape[0]):
            row = new_df.iloc[idx, :]
            if row.isna().any():
                for feature in range(new_df.shape[1]):
                    if not pd.isna(row.iloc[feature]):
                        self.deleted_values[feature].append(row.iloc[feature])

        new_df = new_df.dropna()
        new_df.set_index(self.index[max(self.orders_diff.values()):], inplace=True)
        return new_df

    def inverse_transform(self, X, y=None):
        """
        Deshace las diferenciaciones aplicadas, restaurando los valores originales.

        Parámetros:
        -----------
        X : DataFrame
            Los datos transformados de los cuales se quieren recuperar los valores originales.

        y : None
            No utilizado.

        Retorna:
        --------
        reconstructed_df : DataFrame
            Los datos restaurados a su forma original antes de la transformación.
        """
        reconstructed_df = pd.DataFrame(columns=self.columns)
        for feature, order in self.orders_diff.items():
            series = X.iloc[:, feature]
            if order == 0:
                for current_order in range(max(self.orders_diff.values())):
                    series = np.insert(series, 0, self.deleted_values[feature][current_order])
            else:
                for current_order in range(max(self.orders_diff.values())):
                    series = np.cumsum(np.insert(series, 0, self.deleted_values[feature][current_order]))
            reconstructed_df[self.columns[feature]] = series
        return reconstructed_df


class WindowedTransformer(BaseEstimator, TransformerMixin):
    """
    Clase para dividir un DataFrame en dos arrays de ventanas de datos, uno de predictores y otro de etiquetas, 
    basándose en el número de timesteps (n_past y n_future). Este transformador es útil para tareas de predicción de series de tiempo 
    donde se requiere dividir el dataset en ventanas de observaciones pasadas y futuras.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.

    Atributos:
    ----------
    n_past : int
        Número de pasos de tiempo pasados a usar como predictores.
    
    n_future : int
        Número de pasos de tiempo futuros a usar como etiquetas.

    Métodos:
    --------
    __init__(n_past, n_future):
        Inicializa la clase con los timesteps para predictores y etiquetas.
    
    fit(X, y=None):
        Guarda los nombres de las columnas del DataFrame para su posterior uso.
    
    transform(X_input, y=None):
        Genera dos arrays: uno con las ventanas de datos pasados (predictores) y otro con los futuros (etiquetas).
    
    inverse_transform(Xt, y=None):
        Reconstruye un DataFrame a partir de los arrays de ventanas de predictores y etiquetas.
    """

    def __init__(self, n_past, n_future):
        """
        Inicializa la clase WindowedTransformer con el número de timesteps para los predictores y etiquetas.

        Parámetros:
        -----------
        n_past : int
            El número de pasos de tiempo pasados que se utilizarán como predictores.
        
        n_future : int
            El número de pasos de tiempo futuros que se utilizarán como etiquetas.
        """
        self.n_past = n_past
        self.n_future = n_future

    def fit(self, X, y=None):
        """
        Ajusta el transformador almacenando los nombres de las columnas del DataFrame para su posterior uso.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos de entrada con características temporales.
        
        y : None
            No utilizado.

        Retorna:
        --------
        self : WindowedTransformer
            El propio objeto para permitir el encadenamiento.
        """
        self.columns = X.columns
        #self.index = X.index
        return self
        
    def transform(self, X_input, y=None):
        """
        Divide el DataFrame en ventanas de datos. El resultado es una tupla de dos arrays: uno con las ventanas de
        los datos pasados (predictores) y otro con las ventanas de los datos futuros (etiquetas).

        Parámetros:
        -----------
        X_input : pd.DataFrame
            El conjunto de datos de entrada con características temporales.

        y : None
            No utilizado.

        Retorna:
        --------
        tuple : (np.array, np.array)
            - El primer array contiene las ventanas de los datos pasados (predictores).
            - El segundo array contiene las ventanas de los datos futuros (etiquetas), con forma ajustada según las características.
        """
        if (X_input.shape[0] <= self.n_past):
            print ('Input shape not big enough for given n_past')
            return None, None
        elif (X_input.shape[0] <= self.n_future):
            print ('Input shape not big enough for given n_future')
            return None, None
        X = []
        Ys = []
        for i in range(self.n_past, len(np.array(X_input)) + 1 - self.n_future):
            X.append(np.array(X_input)[i - self.n_past : i, 0 : np.array(X_input).shape[1]])
        
        for layer in range(np.array(X_input).shape[1]):
            Y = []
            for i in range(self.n_past, len(np.array(X_input)) + 1 - self.n_future):
                Y.append(np.array(X_input)[i : i + self.n_future, layer])
            Ys.append(np.array(Y))

        X, Ys = np.array(X), np.array(Ys)
        Ys = Ys.transpose(1, 2, 0)
        return (X, Ys)

    def inverse_transform(self, Xt, y=None):
        """
        Reconstruye un DataFrame a partir de dos arrays de ventanas de predictores y etiquetas.
        Combina las ventanas pasadas y futuras para crear una secuencia de datos continua.

        Parámetros:
        -----------
        Xt : tuple
            Una tupla que contiene:
            - El primer array con las ventanas de predictores.
            - El segundo array con las ventanas de etiquetas.
        
        y : None
            No utilizado.

        Retorna:
        --------
        itransformed_df : pd.DataFrame
            El DataFrame reconstruido a partir de las ventanas de predictores y etiquetas.
        """
        X, Ys = Xt
        itransformed_df = pd.DataFrame()

        for layer in range(X.shape[2]):
            itransformed_df[layer] = np.concatenate(
                (np.concatenate((X[0, :, layer], Ys[0, :, layer])), Ys[1:, -1, layer])
            )
        itransformed_df.columns = self.columns
        #itransformed_df.index = self.index
        return itransformed_df


class StandardScalerAdapter(BaseEstimator, TransformerMixin):
    """
    Adaptador personalizado para aplicar la estandarización a cada columna
    de un DataFrame de forma independiente utilizando `StandardScaler` de scikit-learn.

    Esta clase permite aplicar transformaciones de estandarización (media 0 y desviación estándar 1)
    a cada columna de un DataFrame. Es útil para mantener las propiedades de cada característica
    individual, especialmente cuando se trabaja con DataFrames que tienen múltiples columnas.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.

    Atributos:
    ----------
    columns : pd.Index
        Almacena los nombres de las columnas del DataFrame para ser reutilizadas en las transformaciones.
    
    scalers : dict
        Diccionario que almacena un objeto `StandardScaler` de scikit-learn para cada columna del DataFrame.

    Métodos:
    --------
    fit(X, y=None):
        Ajusta un `StandardScaler` para cada columna del DataFrame.
    
    transform(X, y=None):
        Aplica la estandarización a cada columna utilizando los escaladores ajustados.
    
    inverse_transform(X, y=None):
        Revierte la estandarización, devolviendo los datos a sus valores originales.
    """

    def fit(self, X, y=None):
        """
        Ajusta un `StandardScaler` para cada columna del DataFrame. 
        Se almacena un escalador para cada columna para su posterior uso en la transformación.

        Parámetros:
        -----------
        X : pd.DataFrame
            El DataFrame cuyas columnas se van a estandarizar.
        
        y : None
            No utilizado, mantenido para compatibilidad con otras clases de scikit-learn.

        Retorna:
        --------
        self : StandardScalerAdapter
            El propio objeto ajustado, necesario para el patrón de scikit-learn fit/transform.
        """
        self.columns = X.columns
        #self.index = X.index
        self.scalers = {}
        for column in range(X.values.shape[1]):
            scaler = StandardScaler()
            scaler.fit(X.values[:, column].reshape(-1, 1))
            self.scalers[column] = scaler
        
        return self

    def transform(self, X, y=None):
        """
        Transforma los datos estandarizando cada columna utilizando los escaladores previamente ajustados.

        Parámetros:
        -----------
        X : pd.DataFrame
            El DataFrame que se va a transformar.
        
        y : None
            No utilizado, mantenido para compatibilidad con otras clases de scikit-learn.

        Retorna:
        --------
        pd.DataFrame : DataFrame transformado con las mismas columnas originales,
        pero con los valores estandarizados (media 0 y desviación estándar 1).
        """
        transformed_X = X.values.copy()
        for column in range(X.values.shape[1]):
            transformed_X[:, column] = self.scalers[column].transform(X.values[:, column].reshape(-1, 1)).flatten()
        return pd.DataFrame(transformed_X, columns=self.columns)

    def inverse_transform(self, X, y=None):
        """
        Deshace la transformación (escalado) y devuelve los valores a su escala original.

        Parámetros:
        -----------
        X : pd.DataFrame
            El DataFrame transformado que se quiere revertir a sus valores originales.
        
        y : None
            No utilizado, mantenido para compatibilidad con otras clases de scikit-learn.

        Retorna:
        --------
        pd.DataFrame : DataFrame con los valores originales desescalados.
        """
        itransformed_X = X.values.copy()
        for column in range(X.values.shape[1]):
            itransformed_X[:, column] = self.scalers[column].inverse_transform(X.values[:, column].reshape(-1, 1)).flatten()
        return pd.DataFrame(itransformed_X, columns=self.columns)#, index=self.index)


class StationatersEnsemble(BaseEstimator, TransformerMixin):
    """
    Clase para aplicar múltiples "estacionadores" secuencialmente sobre un DataFrame.
    Esto es útil cuando, al intentar estacionar series temporales, algunas de las series pueden necesitar
    más de un proceso de diferenciación para volverse estacionarias.

    El objetivo es empaquetar varios estacionadores y aplicar un conjunto de transformaciones
    para asegurar que todas las series en el DataFrame se vuelvan estacionarias.

    Hereda de:
    ----------
    BaseEstimator : Clase base para estimadores de scikit-learn.
    TransformerMixin : Clase que añade el método 'fit_transform' para transformadores.

    Atributos:
    ----------
    threshold : float
        Umbral de significancia para determinar si una serie temporal es estacionaria.
    
    diff_limit : int
        Límite máximo de diferenciaciones que puede aplicar cada estacionador individual a una serie temporal.
    
    stationaters_limit : int
        Límite máximo de estacionadores que pueden ser aplicados secuencialmente.

    Métodos:
    --------
    __init__(threshold, diff_limit, stationaters_limit):
        Inicializa la clase con el umbral de significancia, el límite de diferenciaciones y el límite de estacionadores.
    
    fit(X, y=None):
        Ajusta múltiples estacionadores secuenciales al DataFrame para asegurar que todas las series sean estacionarias.
    
    transform(X, y=None):
        Aplica las transformaciones de los estacionadores ajustados al DataFrame para hacerlo estacionario.
    
    inverse_transform(X, y=None):
        Revierte las transformaciones aplicadas por los estacionadores, restaurando el DataFrame a su forma original.
    """

    def __init__(self, threshold, diff_limit, stationaters_limit):
        """
        Inicializa la clase StationatersEnsemble con el umbral de significancia para la estacionariedad, el límite
        de diferenciación para cada estacionador y el límite máximo de estacionadores.

        Parámetros:
        -----------
        threshold : float
            El umbral de significancia para evaluar la estacionariedad de las series temporales.
        
        diff_limit : int
            El límite máximo de diferenciaciones que se permite aplicar a cada serie temporal por estacionador.
        
        stationaters_limit : int
            El límite máximo de estacionadores que pueden ser aplicados de forma secuencial.
        """
        self.threshold = threshold
        self.diff_limit = diff_limit
        self.stationaters_limit = stationaters_limit

    def fit(self, X, y=None):
        """
        Ajusta múltiples estacionadores secuenciales al DataFrame. Para cada columna (serie temporal) del DataFrame,
        se aplica un proceso de diferenciación (estacionador) hasta que todas las series sean estacionarias o hasta
        que se alcance el límite de estacionadores.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos de entrada con características temporales.
        
        y : None
            No utilizado.

        Retorna:
        --------
        self : StationatersEnsemble
            El propio objeto ajustado, necesario para el patrón de scikit-learn fit/transform.
        """
        evaluator = StationarityTester(threshold=self.threshold)
        self.stationaters = {}
        evaluations = [evaluator.evaluate(X[feature]) for feature in X]

        current_stationated_X = X.copy()
        order = 0
        while any(evaluations):
            if order == self.stationaters_limit:
                print('Stationaters limit reached')
                break
            current_stationater = Stationater(threshold=self.threshold, diff_limit=self.diff_limit)
            current_stationated_X = current_stationater.fit_transform(current_stationated_X)
            self.stationaters[order] = current_stationater
            evaluations = [evaluator.evaluate(current_stationated_X[feature]) for feature in X]
            order += 1
        return self

    def transform(self, X, y=None):
        """
        Aplica las transformaciones de los estacionadores ajustados al DataFrame.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos a transformar.

        y : None
            No utilizado.

        Retorna:
        --------
        pd.DataFrame : El DataFrame transformado con las series temporales estacionarias.
        """
        if len(self.stationaters) == 0:
            return X

        current_stationated_X = X.copy()
        for stationater in self.stationaters.values():
            current_stationated_X = stationater.transform(current_stationated_X)
        
        return current_stationated_X

    def inverse_transform(self, X, y=None):
        """
        Revierte las transformaciones aplicadas por los estacionadores, devolviendo el DataFrame a su forma original.

        Parámetros:
        -----------
        X : pd.DataFrame
            El conjunto de datos transformados que se desea revertir.

        y : None
            No utilizado.

        Retorna:
        --------
        pd.DataFrame : El DataFrame restaurado con las series temporales en su forma original.
        """
        current_inverse_transformed_X = X.copy()
        
        if len(self.stationaters) == 0:
            return X

        for stationater in reversed(self.stationaters.values()):
            current_inverse_transformed_X = stationater.inverse_transform(current_inverse_transformed_X)
        
        return current_inverse_transformed_X

def split_simple(df, porcentaje_separacion_train, porcentaje_separacion_val):
    """
    Divide el DataFrame en conjuntos de entrenamiento, validación y prueba de manera temporal simple.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        porcentaje_separacion_train (float): Porcentaje de datos que se utilizarán para entrenamiento (entre 0 y 1).
        porcentaje_separacion_val (float): Porcentaje de datos que se utilizarán para validación (entre 0 y 1).
    Returns:
        tuple: Conjunto de entrenamiento, conjunto de validación y conjunto de prueba.
    """
    q1 = int(len(df) * porcentaje_separacion_train)
    q2 = int(len(df) * (porcentaje_separacion_train + porcentaje_separacion_val))
    
    train = df.iloc[:q1].copy()
    val = df.iloc[q1:q2].copy()
    test = df.iloc[q2:].copy()
    
    return train, val, test

def split_time_series_cv(df, n_splits):
    """
    Realiza una validación cruzada para series temporales, dividiendo los datos en n_splits pliegues.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        n_splits (int): Número de pliegues para la validación cruzada.
        
    Returns:
        list of tuple: Lista de pares (entrenamiento, prueba) para cada pliegue.
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    splits = []
    for train_index, test_index in tscv.split(df):
        train, test = df.iloc[train_index].copy(), df.iloc[test_index].copy()
        splits.append((train, test))
    return splits
    
def split_sliding_window(df, train_size, test_size, step_size):
    """
    Divide el DataFrame utilizando una ventana deslizante para entrenamiento y prueba.
    
    Args:
        df (pd.DataFrame): DataFrame que contiene los datos.
        train_size (int): Tamaño de la ventana de entrenamiento.
        test_size (int): Tamaño de la ventana de prueba.
        step_size (int): Número de pasos para mover la ventana.
        
    Returns:
        list of tuple: Lista de pares (entrenamiento, prueba) para cada ventana.
    """
    splits = []
    for start in range(0, len(df) - train_size - test_size + 1, step_size):
        train = df.iloc[start:start + train_size].copy()
        test = df.iloc[start + train_size:start + train_size + test_size].copy()
        splits.append((train, test))
    return splits
