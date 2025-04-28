from fastapi import FastAPI
from app.routes import user, question, food_update, behavior, goal, tips, big_five
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/auth", tags=["Authentication"])
app.include_router(question.router, prefix="/question", tags=["question"])
app.include_router(behavior.router, prefix="/behavior", tags=["behavior"])
app.include_router(goal.router, prefix="/goal", tags=["goal"])
app.include_router(tips.router, prefix="/tips", tags=["tips"])
app.include_router(food_update.router, prefix="/food-update", tags=["food_update"])
app.include_router(big_five.router, prefix="/big-five", tags=["big_five"])


@app.get("/")
def root():
    return {"message": "API is running!"}
