import unittest
import numpy as np
import libpysal
import spreg.diagnostics as D
from spreg.twosls_sp import BaseGM_Lag, GM_Lag
from libpysal.common import RTOL

class TestBaseGMLag(unittest.TestCase):
    def setUp(self):
        self.w = libpysal.weights.Rook.from_shapefile(libpysal.examples.get_path("columbus.shp"))
        self.w.transform = 'r'
        self.db = libpysal.io.open(libpysal.examples.get_path("columbus.dbf"), 'r')
        y = np.array(self.db.by_col("HOVAL"))
        self.y = np.reshape(y, (49,1))
        
    def test___init__(self):
        w_lags = 2
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        #yd2, q2 = spreg.utils.set_endog(self.y, self.X, self.w, None, None, w_lags, True)
        self.X = np.hstack((np.ones(self.y.shape),self.X))
        reg = BaseGM_Lag(self.y, self.X, w=self.w, w_lags=w_lags)
        betas = np.array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        h_0 = np.array([  1.        ,  19.531     ,  15.72598   ,  18.594     ,
                            24.7142675 ,  13.72216667,  27.82929567])
        np.testing.assert_allclose(reg.h[0], h_0)
        hth = np.  array([   49.        ,   704.371999  ,  1721.312371  ,   724.7435916 ,
                             1707.35412945,   711.31248483,  1729.63201243])
        np.testing.assert_allclose(reg.hth[0], hth,RTOL)
        hthi = np.array([  7.33701328e+00,   2.27764882e-02,   2.18153588e-02,
                           -5.11035447e-02,   1.22515181e-03,  -2.38079378e-01,
                           -1.20149133e-01])
        np.testing.assert_allclose(reg.hthi[0], hthi,RTOL)
        self.assertEqual(reg.k, 4)
        self.assertEqual(reg.kstar, 1)
        np.testing.assert_allclose(reg.mean_y, 38.436224469387746,RTOL)
        self.assertEqual(reg.n, 49)
        pfora1a2 = np.array([ 80.5588479 ,  -1.06625281,  -0.61703759,  -1.10071931]) 
        np.testing.assert_allclose(reg.pfora1a2[0], pfora1a2,RTOL)
        predy_5 = np.array([[ 50.87411532],[ 50.76969931],[ 41.77223722],[ 33.44262382],[ 28.77418036]])
        np.testing.assert_allclose(reg.predy[0:5], predy_5,RTOL)
        q_5 = np.array([ 18.594     ,  24.7142675 ,  13.72216667,  27.82929567])
        np.testing.assert_allclose(reg.q[0], q_5)
        np.testing.assert_allclose(reg.sig2n_k, 234.54258763039289,RTOL)
        np.testing.assert_allclose(reg.sig2n, 215.39625394627919,RTOL)
        np.testing.assert_allclose(reg.sig2, 215.39625394627919,RTOL)
        np.testing.assert_allclose(reg.std_y, 18.466069465206047,RTOL)
        u_5 = np.array( [[ 29.59288768], [ -6.20269831], [-15.42223722], [ -0.24262282], [ -5.54918036]])
        np.testing.assert_allclose(reg.u[0:5], u_5,RTOL)
        np.testing.assert_allclose(reg.utu, 10554.41644336768,RTOL)
        varb = np.array( [[  1.48966377e+00, -2.28698061e-02, -1.20217386e-02, -1.85763498e-02],
                          [ -2.28698061e-02,  1.27893998e-03,  2.74600023e-04, -1.33497705e-04],
                          [ -1.20217386e-02,  2.74600023e-04,  1.54257766e-04,  6.86851184e-05],
                          [ -1.85763498e-02, -1.33497705e-04,  6.86851184e-05,  4.67711582e-04]])
        np.testing.assert_allclose(reg.varb, varb,RTOL)
        vm = np.array([[  3.20867996e+02, -4.92607057e+00, -2.58943746e+00, -4.00127615e+00],
                       [ -4.92607057e+00,  2.75478880e-01,  5.91478163e-02, -2.87549056e-02],
                       [ -2.58943746e+00,  5.91478163e-02,  3.32265449e-02,  1.47945172e-02],
                       [ -4.00127615e+00, -2.87549056e-02,  1.47945172e-02,  1.00743323e-01]])
        np.testing.assert_allclose(reg.vm, vm,RTOL)
        x_0 = np.array([  1.     ,  19.531  ,  15.72598])
        np.testing.assert_allclose(reg.x[0], x_0,RTOL)
        y_5 = np.array( [[ 80.467003], [ 44.567001], [ 26.35    ], [ 33.200001], [ 23.225   ]])
        np.testing.assert_allclose(reg.y[0:5], y_5,RTOL)
        yend_5 = np.array( [[ 35.4585005 ], [ 46.67233467], [ 45.36475125], [ 32.81675025], [ 30.81785714]])
        np.testing.assert_allclose(reg.yend[0:5], yend_5,RTOL)
        z_0 = np.array([  1.       ,  19.531    ,  15.72598  ,  35.4585005]) 
        np.testing.assert_allclose(reg.z[0], z_0,RTOL)
        zthhthi = np.array( [[  1.00000000e+00, -2.22044605e-16, -2.22044605e-16 , 2.22044605e-16,
                                4.44089210e-16,  0.00000000e+00, -8.88178420e-16],
                             [  0.00000000e+00,  1.00000000e+00, -3.55271368e-15 , 3.55271368e-15,
                               -7.10542736e-15,  7.10542736e-14,  0.00000000e+00],
                             [  1.81898940e-12,  2.84217094e-14,  1.00000000e+00 , 0.00000000e+00,
                               -2.84217094e-14,  5.68434189e-14,  5.68434189e-14],
                             [ -8.31133940e+00, -3.76104678e-01, -2.07028208e-01 , 1.32618931e+00,
                               -8.04284562e-01,  1.30527047e+00,  1.39136816e+00]])
        # np.testing.assert_allclose(reg.zthhthi, zthhthi, RTOL) WHYYYY
        np.testing.assert_array_almost_equal(reg.zthhthi, zthhthi, 7)

    def test_init_white_(self):
        w_lags = 2
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        #yd2, q2 = spreg.utils.set_endog(self.y, self.X, self.w, None, None, w_lags, True)
        self.X = np.hstack((np.ones(self.y.shape),self.X))
        base_gm_lag = BaseGM_Lag(self.y, self.X, w=self.w, w_lags=w_lags, robust='white')
        tbetas = np.array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(base_gm_lag.betas, tbetas) 
        dbetas = D.se_betas(base_gm_lag)
        se_betas = np.array([ 20.47077481, 0.50613931, 0.20138425, 0.38028295 ])
        np.testing.assert_allclose(dbetas, se_betas)

    def test_init_hac_(self):
        w_lags = 2
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        #yd2, q2 = spreg.utils.set_endog(self.y, self.X, self.w, None, None, w_lags, True)
        self.X = np.hstack((np.ones(self.y.shape),self.X))
        gwk = libpysal.weights.Kernel.from_shapefile(libpysal.examples.get_path('columbus.shp'),k=15,function='triangular', fixed=False)        
        base_gm_lag = BaseGM_Lag(self.y, self.X, w=self.w, w_lags=w_lags, robust='hac', gwk=gwk)
        tbetas = np.array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(base_gm_lag.betas, tbetas) 
        dbetas = D.se_betas(base_gm_lag)
        se_betas = np.array([ 19.08513569,   0.51769543,   0.18244862,   0.35460553])
        np.testing.assert_allclose(dbetas, se_betas)

    def test_init_discbd(self):
        w_lags = 2
        X = np.array(self.db.by_col("INC"))
        self.X = np.reshape(X, (49,1))
        yd = np.array(self.db.by_col("CRIME"))
        yd = np.reshape(yd, (49,1))
        q = np.array(self.db.by_col("DISCBD"))
        q = np.reshape(q, (49,1))
        #yd2, q2 = spreg.utils.set_endog(self.y, self.X, self.w, yd, q, w_lags, True)
        self.X = np.hstack((np.ones(self.y.shape),self.X))
        reg = BaseGM_Lag(self.y, self.X, w=self.w, yend=yd, q=q, w_lags=w_lags)
        tbetas = np.array([[ 100.79359082], [  -0.50215501], [  -1.14881711], [  -0.38235022]])
        np.testing.assert_allclose(tbetas, reg.betas)
        dbetas = D.se_betas(reg)
        se_betas = np.array([ 53.0829123 ,   1.02511494,   0.57589064,   0.59891744 ])
        np.testing.assert_allclose(dbetas, se_betas)

    def test_n_k(self):
        w_lags = 2
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        #yd2, q2 = spreg.utils.set_endog(self.y, self.X, self.w, None, None, w_lags, True)
        self.X = np.hstack((np.ones(self.y.shape),self.X))
        reg = BaseGM_Lag(self.y, self.X, w=self.w, w_lags=w_lags, sig2n_k=True)
        betas = np.  array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        vm = np.array( [[  3.49389596e+02, -5.36394351e+00, -2.81960968e+00, -4.35694515e+00],
                         [ -5.36394351e+00,  2.99965892e-01,  6.44054000e-02, -3.13108972e-02],
                         [ -2.81960968e+00,  6.44054000e-02,  3.61800155e-02,  1.61095854e-02],
                         [ -4.35694515e+00, -3.13108972e-02,  1.61095854e-02,  1.09698285e-01]])
        np.testing.assert_allclose(reg.vm, vm,RTOL)

    def test_lag_q(self):
        w_lags = 2
        X = np.array(self.db.by_col("INC"))
        self.X = np.reshape(X, (49,1))
        yd = np.array(self.db.by_col("CRIME"))
        yd = np.reshape(yd, (49,1))
        q = np.array(self.db.by_col("DISCBD"))
        q = np.reshape(q, (49,1))
        #yd2, q2 = spreg.utils.set_endog(self.y, self.X, self.w, yd, q, w_lags, False)
        self.X = np.hstack((np.ones(self.y.shape),self.X))
        reg = BaseGM_Lag(self.y, self.X, w=self.w, yend=yd, q=q, w_lags=w_lags, lag_q=False)
        tbetas = np.array( [[ 108.83261383], [  -0.48041099], [  -1.18950006], [  -0.56140186]])
        np.testing.assert_allclose(tbetas, reg.betas)
        dbetas = D.se_betas(reg)
        se_betas = np.array([ 58.33203837,   1.09100446,   0.62315167,   0.68088777])
        np.testing.assert_allclose(dbetas, se_betas)



class TestGMLag(unittest.TestCase):
    def setUp(self):
        self.w = libpysal.weights.Rook.from_shapefile(libpysal.examples.get_path("columbus.shp"))
        self.w.transform = 'r'
        self.w2 = libpysal.weights.Queen.from_shapefile(libpysal.examples.get_path('columbus.shp'))
        self.db = libpysal.io.open(libpysal.examples.get_path("columbus.dbf"), 'r')
        y = np.array(self.db.by_col("HOVAL"))
        self.y = np.reshape(y, (49,1))
        
    def test___init__(self):
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        reg = GM_Lag(self.y, self.X, w=self.w, w_lags=2)
        betas = np.array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        e_5 = np.array( [[ 29.28976367], [ -6.07439501], [-15.30080685], [ -0.41773375], [ -5.67197968]])
        np.testing.assert_allclose(reg.e_pred[0:5], e_5,RTOL)
        h_0 = np.array([  1.        ,  19.531     ,  15.72598   ,  18.594     ,
                            24.7142675 ,  13.72216667,  27.82929567])
        np.testing.assert_allclose(reg.h[0], h_0)
        hth = np.  array([   49.        ,   704.371999  ,  1721.312371  ,   724.7435916 ,
                             1707.35412945,   711.31248483,  1729.63201243])
        np.testing.assert_allclose(reg.hth[0], hth,RTOL)
        hthi = np.array([  7.33701328e+00,   2.27764882e-02,   2.18153588e-02,
                           -5.11035447e-02,   1.22515181e-03,  -2.38079378e-01,
                           -1.20149133e-01])
        np.testing.assert_allclose(reg.hthi[0], hthi,RTOL)
        self.assertEqual(reg.k, 4)
        self.assertEqual(reg.kstar, 1)
        np.testing.assert_allclose(reg.mean_y, 38.436224469387746,RTOL)
        self.assertEqual(reg.n, 49)
        pfora1a2 = np.array([ 80.5588479 ,  -1.06625281,  -0.61703759,  -1.10071931]) 
        np.testing.assert_allclose(reg.pr2, 0.3551928222612527,RTOL)
        np.testing.assert_allclose(reg.pr2_e, 0.34763857386174174,RTOL)
        np.testing.assert_allclose(reg.pfora1a2[0], pfora1a2,RTOL)
        predy_5 = np.array([[ 50.87411532],[ 50.76969931],[ 41.77223722],[ 33.44262382],[ 28.77418036]])
        np.testing.assert_allclose(reg.predy[0:5], predy_5,RTOL)
        predy_e_5 = np.array( [[ 51.17723933], [ 50.64139601], [ 41.65080685], [ 33.61773475], [ 28.89697968]])
        np.testing.assert_allclose(reg.predy_e[0:5], predy_e_5,RTOL)
        q_5 = np.array([ 18.594     ,  24.7142675 ,  13.72216667,  27.82929567])
        np.testing.assert_allclose(reg.q[0], q_5)
        self.assertEqual(reg.robust, 'unadjusted')
        np.testing.assert_allclose(reg.sig2n_k, 234.54258763039289,RTOL)
        np.testing.assert_allclose(reg.sig2n, 215.39625394627919,RTOL)
        np.testing.assert_allclose(reg.sig2, 215.39625394627919,RTOL)
        np.testing.assert_allclose(reg.std_y, 18.466069465206047,RTOL)
        u_5 = np.array( [[ 29.59288768], [ -6.20269831], [-15.42223722], [ -0.24262282], [ -5.54918036]])
        np.testing.assert_allclose(reg.u[0:5], u_5,RTOL)
        np.testing.assert_allclose(reg.utu, 10554.41644336768,RTOL)
        varb = np.array( [[  1.48966377e+00, -2.28698061e-02, -1.20217386e-02, -1.85763498e-02],
                          [ -2.28698061e-02,  1.27893998e-03,  2.74600023e-04, -1.33497705e-04],
                          [ -1.20217386e-02,  2.74600023e-04,  1.54257766e-04,  6.86851184e-05],
                          [ -1.85763498e-02, -1.33497705e-04,  6.86851184e-05,  4.67711582e-04]])
        np.testing.assert_allclose(reg.varb, varb,RTOL)
        vm = np.array([[  3.20867996e+02, -4.92607057e+00, -2.58943746e+00, -4.00127615e+00],
                       [ -4.92607057e+00,  2.75478880e-01,  5.91478163e-02, -2.87549056e-02],
                       [ -2.58943746e+00,  5.91478163e-02,  3.32265449e-02,  1.47945172e-02],
                       [ -4.00127615e+00, -2.87549056e-02,  1.47945172e-02,  1.00743323e-01]])
        np.testing.assert_allclose(reg.vm, vm,RTOL)
        x_0 = np.array([  1.     ,  19.531  ,  15.72598])
        np.testing.assert_allclose(reg.x[0], x_0,RTOL)
        y_5 = np.array( [[ 80.467003], [ 44.567001], [ 26.35    ], [ 33.200001], [ 23.225   ]])
        np.testing.assert_allclose(reg.y[0:5], y_5,RTOL)
        yend_5 = np.array( [[ 35.4585005 ], [ 46.67233467], [ 45.36475125], [ 32.81675025], [ 30.81785714]])
        np.testing.assert_allclose(reg.yend[0:5], yend_5,RTOL)
        z_0 = np.array([  1.       ,  19.531    ,  15.72598  ,  35.4585005]) 
        np.testing.assert_allclose(reg.z[0], z_0,RTOL)
        zthhthi = np.array( [[  1.00000000e+00, -2.22044605e-16, -2.22044605e-16 , 2.22044605e-16,
                                4.44089210e-16,  0.00000000e+00, -8.88178420e-16],
                             [  0.00000000e+00,  1.00000000e+00, -3.55271368e-15 , 3.55271368e-15,
                               -7.10542736e-15,  7.10542736e-14,  0.00000000e+00],
                             [  1.81898940e-12,  2.84217094e-14,  1.00000000e+00 , 0.00000000e+00,
                               -2.84217094e-14,  5.68434189e-14,  5.68434189e-14],
                             [ -8.31133940e+00, -3.76104678e-01, -2.07028208e-01 , 1.32618931e+00,
                               -8.04284562e-01,  1.30527047e+00,  1.39136816e+00]])
        # np.testing.assert_allclose(reg.zthhthi, zthhthi RTOL) #another issue with rtol
        np.testing.assert_array_almost_equal(reg.zthhthi, zthhthi, 7)

    def test_init_white_(self):
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        base_gm_lag = GM_Lag(self.y, self.X, w=self.w, w_lags=2, robust='white')
        tbetas = np.array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(base_gm_lag.betas, tbetas) 
        dbetas = D.se_betas(base_gm_lag)
        se_betas = np.array([ 20.47077481, 0.50613931, 0.20138425, 0.38028295 ])
        np.testing.assert_allclose(dbetas, se_betas)

    def test_init_hac_(self):
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        gwk = libpysal.weights.Kernel.from_shapefile(libpysal.examples.get_path('columbus.shp'),k=15,function='triangular', fixed=False)        
        base_gm_lag = GM_Lag(self.y, self.X, w=self.w, w_lags=2, robust='hac', gwk=gwk)
        tbetas = np.array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(base_gm_lag.betas, tbetas) 
        dbetas = D.se_betas(base_gm_lag)
        se_betas = np.array([ 19.08513569,   0.51769543,   0.18244862,   0.35460553])
        np.testing.assert_allclose(dbetas, se_betas)

    def test_init_discbd(self):
        X = np.array(self.db.by_col("INC"))
        X = np.reshape(X, (49,1))
        yd = np.array(self.db.by_col("CRIME"))
        yd = np.reshape(yd, (49,1))
        q = np.array(self.db.by_col("DISCBD"))
        q = np.reshape(q, (49,1))
        reg = GM_Lag(self.y, X, w=self.w, yend=yd, q=q, w_lags=2)
        tbetas = np.array([[ 100.79359082], [  -0.50215501], [  -1.14881711], [  -0.38235022]])
        np.testing.assert_allclose(tbetas, reg.betas)
        dbetas = D.se_betas(reg)
        se_betas = np.array([ 53.0829123 ,   1.02511494,   0.57589064,   0.59891744 ])
        np.testing.assert_allclose(dbetas, se_betas)

    def test_n_k(self):
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        reg = GM_Lag(self.y, self.X, w=self.w, w_lags=2, sig2n_k=True)
        betas = np.  array([[  4.53017056e+01], [  6.20888617e-01], [ -4.80723451e-01], [  2.83622122e-02]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        vm = np.array( [[  3.49389596e+02, -5.36394351e+00, -2.81960968e+00, -4.35694515e+00],
                         [ -5.36394351e+00,  2.99965892e-01,  6.44054000e-02, -3.13108972e-02],
                         [ -2.81960968e+00,  6.44054000e-02,  3.61800155e-02,  1.61095854e-02],
                         [ -4.35694515e+00, -3.13108972e-02,  1.61095854e-02,  1.09698285e-01]])
        np.testing.assert_allclose(reg.vm, vm,RTOL)

    def test_lag_q(self):
        X = np.array(self.db.by_col("INC"))
        X = np.reshape(X, (49,1))
        yd = np.array(self.db.by_col("CRIME"))
        yd = np.reshape(yd, (49,1))
        q = np.array(self.db.by_col("DISCBD"))
        q = np.reshape(q, (49,1))
        reg = GM_Lag(self.y, X, w=self.w, yend=yd, q=q, w_lags=2, lag_q=False)
        tbetas = np.array( [[ 108.83261383], [  -0.48041099], [  -1.18950006], [  -0.56140186]])
        np.testing.assert_allclose(tbetas, reg.betas)
        dbetas = D.se_betas(reg)
        se_betas = np.array([ 58.33203837,   1.09100446,   0.62315167,   0.68088777])
        np.testing.assert_allclose(dbetas, se_betas)

    def test_spatial(self):
        X = np.array(self.db.by_col("INC"))
        X = np.reshape(X, (49,1))
        yd = np.array(self.db.by_col("CRIME"))
        yd = np.reshape(yd, (49,1))
        q = np.array(self.db.by_col("DISCBD"))
        q = np.reshape(q, (49,1))
        reg = GM_Lag(self.y, X, yd, q, spat_diag=True, w=self.w2)
        betas = np.array([[  5.46344924e+01], [  4.13301682e-01], [ -5.92637442e-01], [ -7.40490883e-03]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        vm = np.array( [[  4.45202654e+02, -1.50290275e+01, -6.36557072e+00, -5.71403440e-03],
                        [ -1.50290275e+01,  5.93124683e-01,  2.19169508e-01, -6.70675916e-03],
                        [ -6.36557072e+00,  2.19169508e-01,  1.06577542e-01, -2.96533875e-03],
                        [ -5.71403440e-03, -6.70675916e-03, -2.96533875e-03,  1.15655425e-03]]) 
        np.testing.assert_allclose(reg.vm, vm,RTOL)
        ak_test = np.array([ 2.52597326,  0.11198567])
        np.testing.assert_allclose(reg.ak_test, ak_test,RTOL)

    def test_names(self):
        X = np.array(self.db.by_col("INC"))
        X = np.reshape(X, (49,1))
        yd = np.array(self.db.by_col("CRIME"))
        yd = np.reshape(yd, (49,1))
        q = np.array(self.db.by_col("DISCBD"))
        q = np.reshape(q, (49,1))
        gwk = libpysal.weights.Kernel.from_shapefile(libpysal.examples.get_path('columbus.shp'),k=5,function='triangular', fixed=False)
        name_x = ['inc']
        name_y = 'crime'
        name_yend = ['crime']
        name_q = ['discbd']
        name_w = 'queen'
        name_gwk = 'k=5'
        name_ds = 'columbus'
        reg = GM_Lag(self.y, X, yd, q,
                spat_diag=True, w=self.w2, robust='hac', gwk=gwk,
                name_x=name_x, name_y=name_y, name_q=name_q, name_w=name_w,
                name_yend=name_yend, name_gwk=name_gwk, name_ds=name_ds)
        betas = np.array([[  5.46344924e+01], [  4.13301682e-01], [ -5.92637442e-01], [ -7.40490883e-03]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        vm = np.array( [[  5.70817052e+02, -1.83655385e+01, -8.36602575e+00,  2.37538877e-02],
                        [ -1.85224661e+01,  6.53311383e-01,  2.84209566e-01, -6.47694160e-03],
                        [ -8.31105622e+00,  2.78772694e-01,  1.38144928e-01, -3.98175246e-03],
                        [  2.66662466e-02, -6.23783104e-03, -4.11092891e-03,  1.10936528e-03]]) 
        np.testing.assert_allclose(reg.vm, vm,RTOL)
        self.assertListEqual(reg.name_x, ['CONSTANT']+name_x)
        name_yend.append('W_crime')
        self.assertListEqual(reg.name_yend, name_yend)
        name_q.extend(['W_inc', 'W_discbd'])
        self.assertListEqual(reg.name_q, name_q)
        self.assertEqual(reg.name_y, name_y)
        self.assertEqual(reg.name_w, name_w)
        self.assertEqual(reg.name_gwk, name_gwk)
        self.assertEqual(reg.name_ds, name_ds)

    def test_slx(self):
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        reg = GM_Lag(self.y, self.X, slx_lags=1, spat_diag=True, w=self.w2)
        betas = np.array([[41.29886912],
                         [ 0.89735195],
                         [-0.70238066],
                         [-2.67204851],
                         [-0.11340296],
                         [ 1.16663877]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        vm = np.array( [[ 4.52762279e+03, -8.39233459e+01,  4.57574864e+01,  1.33304743e+03,
                           7.66131947e+01, -6.05018197e+02],
                         [-8.39233459e+01,  2.72427983e+00, -4.27333794e-01, -1.81523886e+01,
                          -1.00244932e+00,  8.15816638e+00],
                         [ 4.57574864e+01, -4.27333794e-01,  1.34781526e+00,  2.38492740e+01,
                           1.34429440e+00, -1.07935724e+01],
                         [ 1.33304743e+03, -1.81523886e+01,  2.38492740e+01,  5.33976362e+02,
                           3.05662628e+01, -2.41933825e+02],
                         [ 7.66131947e+01, -1.00244932e+00,  1.34429440e+00,  3.05662628e+01,
                           1.75801008e+00, -1.38579938e+01],
                         [-6.05018197e+02,  8.15816638e+00, -1.07935724e+01, -2.41933825e+02,
                          -1.38579938e+01,  1.09633338e+02]])
        np.testing.assert_allclose(reg.vm, vm,RTOL)
        ak_test = np.array([0.001324, 0.970974])
        np.testing.assert_allclose(reg.ak_test, ak_test,RTOL)
        cfh_test = np.array([0.10818 , 0.947347])
        np.testing.assert_allclose(reg.cfh_test, cfh_test,RTOL)

    def test_graph(self):
        X = []
        X.append(self.db.by_col("INC"))
        X.append(self.db.by_col("CRIME"))
        self.X = np.array(X).T
        reg = GM_Lag(self.y, self.X, slx_lags=1, spat_diag=True, w=libpysal.graph.Graph.from_W(self.w2))
        betas = np.array([[41.29886912],
                         [ 0.89735195],
                         [-0.70238066],
                         [-2.67204851],
                         [-0.11340296],
                         [ 1.16663877]])
        np.testing.assert_allclose(reg.betas, betas,RTOL)
        vm = np.array( [[ 4.52762279e+03, -8.39233459e+01,  4.57574864e+01,  1.33304743e+03,
                           7.66131947e+01, -6.05018197e+02],
                         [-8.39233459e+01,  2.72427983e+00, -4.27333794e-01, -1.81523886e+01,
                          -1.00244932e+00,  8.15816638e+00],
                         [ 4.57574864e+01, -4.27333794e-01,  1.34781526e+00,  2.38492740e+01,
                           1.34429440e+00, -1.07935724e+01],
                         [ 1.33304743e+03, -1.81523886e+01,  2.38492740e+01,  5.33976362e+02,
                           3.05662628e+01, -2.41933825e+02],
                         [ 7.66131947e+01, -1.00244932e+00,  1.34429440e+00,  3.05662628e+01,
                           1.75801008e+00, -1.38579938e+01],
                         [-6.05018197e+02,  8.15816638e+00, -1.07935724e+01, -2.41933825e+02,
                          -1.38579938e+01,  1.09633338e+02]])
        np.testing.assert_allclose(reg.vm, vm,RTOL)
        ak_test = np.array([0.001324, 0.970974])
        np.testing.assert_allclose(reg.ak_test, ak_test,RTOL)
        cfh_test = np.array([0.10818 , 0.947347])
        np.testing.assert_allclose(reg.cfh_test, cfh_test,RTOL)


if __name__ == '__main__':
    unittest.main()
