from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse

from transition_learning.controller.request_form.sentiment_analysis_request_form import SentimentAnalysisRequestForm
from transition_learning.controller.request_form.transition_learning_predict_request_form import \
    TransitionLearningPredictRequestForm
from transition_learning.service.transition_learning_service_impl import TransitionLearningServiceImpl

transitionLearningRouter = APIRouter()

async def injectTransitionLearningService() -> TransitionLearningServiceImpl:
    return TransitionLearningServiceImpl()

@transitionLearningRouter.post("/transition-learning-predict")
async def predictWithTransitionLearning(transitionLearningPredictRequestForm: TransitionLearningPredictRequestForm,
                                        transitionLearningService: TransitionLearningServiceImpl =
                                        Depends(injectTransitionLearningService)):

    print(f"controller -> predictWithTransitionLearning(): "
          f"transitionLearningPredictRequestForm: {transitionLearningPredictRequestForm}")

    predictedResult = transitionLearningService.predictText(
        transitionLearningPredictRequestForm)

    return JSONResponse(content=predictedResult, status_code=status.HTTP_200_OK)

@transitionLearningRouter.post("/transition-learning-with-sentiment-analysis")
async def transitionLearningWithsentimentAnalysis(sentimentAnalysisRequestForm: SentimentAnalysisRequestForm,
                                                  transitionLearningService: TransitionLearningServiceImpl =
                                                  Depends(injectTransitionLearningService)):
    print(f"controller -> transitionLearningWithsentimentAnalysis(): "
          f"sentimentAnalysisRequestForm: {sentimentAnalysisRequestForm}")

    predictedResult = transitionLearningService.transitionLearningWithsentimentAnalysis(
        sentimentAnalysisRequestForm)

    return JSONResponse(content=predictedResult, status_code=status.HTTP_200_OK)
