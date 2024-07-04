import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

from principal_component_analysis.repository.pca_repository import PrincipalComponentAnalysisRepository


class PrincipalComponentAnalysisRepositoryImpl(PrincipalComponentAnalysisRepository):

    def createPCASample(self):
        numberOfPoints = 333
        numberOfFeatures = 5
        numberOfComponents = 2

        return numberOfPoints, numberOfFeatures, numberOfComponents

    # 공분산은 실제 상관 관계를 분석할 수 있는 아주 좋은 척도임
    # 우리가 모델을 평가할 때 혼동 행렬을 분석 했듯이
    # 각 종속 변수간의 상호 연관성을 파악할 때는 이 공분산 행렬을 보면 됨

    # 공분산 공식은 Convariance(X, y) = 1 / (n - 1) SUM [ (X샘플 - X평균) * (Y샘플 - Y평균) ]
    # 위와 같은 구성을 가지고 있다.
    # 만약 위의 X샘플 - X평균이 이미 정규화되었다면
    # 아래와 같이 데이터 행렬과 데이터 행렬의 전치를 곱하면 된다. (증명은 생략)
    # 결과적으로 공분산 행렬은 m x m 형태의 정방 행렬이 된다.

    # 그러나 아래쪽에서 갑자기 공분산 파트가 납득되지 않는 형태로 구성되는데
    # rand() 함수 자체가 0과 1사이의 균등 분포로 무작위 값을 생성한다.
    # numberOfFeatures가 5에 해당하므로 5 x 5 형태의 정방 행렬이 생성된다.
    # 위의 정규화에 이미 따르고 있으므로 공분산 행렬 계산 시 행렬 * 전치행렬 형태로 구성이 가능하다.
    def configCovariance(self, numberOfFeatures):
        # z변환 (평균이 0, 분산이 1) 이 되도록 구성해줌
        np.random.seed(42)
        covariance = np.random.rand(numberOfFeatures, numberOfFeatures)
        covariance = np.dot(covariance, covariance.transpose())
        print(f"covariance: {covariance}")

        return covariance


    # 아래 코드에서 mean 파트는 특징 모두의 평균을 0으로 만든다 (이 부분은 쉬움)
    # 다중 확률 분포 함수를 구성할 떄는 여러 확률 변수들에 대한 평균이 필요하다.
    def configZeroMean(self, numberOfFeatures):
        mean = np.zeros(numberOfFeatures)
        return mean

    def createMultiVariateNormalDistribution(self, mean, covariance, numberOfPoints):
        return np.random.multivariate_normal(mean, covariance, numberOfPoints)

    def createDataFrame(self, createdMultiVariateData, numberOfFeatures):
        return pd.DataFrame(
            createdMultiVariateData,
            columns=[f'feature_{i}' for i in range(1, numberOfFeatures + 1)])

    # 주성분 분석을 위한 Scikit Learn 라이브러리의 제공 함수입니다.
    # 예로 원래 데이터가 10개의 변수를 가지고 있다면
    # 지정한 n_components의 개수로 주성분 분석을 위한 준비를 해줍니다.
    def readyForAnalysis(self, numberOfComponents):
        return PCA(n_components=numberOfComponents)

    def fitTransform(self, pca, createdDataFrame):
        return pca.fit_transform(createdDataFrame)
    # 훈련할 때만 fit_transform으로 쓰고 예측할 때는 fit만 한다.

