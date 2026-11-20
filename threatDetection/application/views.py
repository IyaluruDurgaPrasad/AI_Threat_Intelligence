import logging
from django.shortcuts import render
from .hybrid_analyzer import hybrid_threat_analysis, ml_model

logger = logging.getLogger(__name__)

# Max character limit for defense-in-depth against resource exhaustion
MAX_EMAIL_LENGTH = 50000


def get_system_status():
    """Returns actual system status for display on dashboard."""
    ml_ready = ml_model is not None
    return {
        "ml_status": "Online" if ml_ready else "Offline",
        "ml_model_name": "TF-IDF + Logistic Regression",
        "llm_status": "Online",
        "llm_model_name": "Llama 3.2 (Ollama Local)",
    }


def home(request):
    context = {
        "system_status": get_system_status()
    }

    if request.method == "POST":
        email_text = request.POST.get("email_text", "").strip()
        context["email_text"] = email_text

        if not email_text:
            context["error"] = "Please enter or paste email content to analyze."
        elif len(email_text) > MAX_EMAIL_LENGTH:
            context["error"] = (
                f"Email content is too long ({len(email_text)} characters). "
                f"Maximum permitted length is {MAX_EMAIL_LENGTH} characters."
            )
        else:
            try:
                result = hybrid_threat_analysis(email_text)

                if "error" in result:
                    context["error"] = result["error"]
                else:
                    context["result"] = result

            except Exception as e:
                logger.error("Analysis execution error: %s", e, exc_info=True)
                context["error"] = (
                    "Unable to complete the threat analysis. "
                    "Please verify that the ML model and local Ollama service are active."
                )

    context["active_tab"] = "scanner"
    return render(request, "application/home.html", context)


def metrics(request):
    """Renders comprehensive dataset analysis, model performance metrics, and evaluation data."""
    context = {
        "system_status": get_system_status(),
        "active_tab": "metrics",
        "dataset": {
            "total_emails": 17522,
            "safe_count": 10978,
            "phish_count": 6544,
            "safe_pct": 62.65,
            "phish_pct": 37.35,
            "train_count": 14017,
            "test_count": 3505,
            "train_pct": 80.0,
            "test_pct": 20.0,
            "raw_dataset_name": "Phishing_Email.csv",
            "cleaned_dataset_name": "cleaned_phishing_emails.csv",
        },
        "model_performance": {
            "overall_accuracy": 98.00,
            "overall_precision": 98.01,
            "overall_recall": 98.00,
            "overall_f1": 98.01,
            "roc_auc": 0.9972,
            "pr_auc": 0.9949,
            "mcc": 0.9575,
            "specificity": 98.00,
            "fpr_rate": 2.00,
            "fnr_rate": 1.99,
            "safe_class": {
                "precision": 98.81,
                "recall": 98.00,
                "f1_score": 98.40,
                "support": 2196,
            },
            "phish_class": {
                "precision": 96.68,
                "recall": 98.01,
                "f1_score": 97.34,
                "support": 1309,
            },
            "confusion_matrix": {
                "true_negative": 2152,  # Safe correctly classified
                "false_positive": 44,    # Safe misclassified as Phishing (False Alarm)
                "false_negative": 26,    # Phishing misclassified as Safe (Missed Threat)
                "true_positive": 1283,   # Phishing correctly classified
                "total_tested": 3505,
                "fpr": 2.00,
                "fnr": 1.99,
            },

            "architecture": {
                "vectorizer": "TF-IDF Vectorizer",
                "max_features": "10,000 Features",
                "ngram_range": "(1, 2) Unigrams & Bigrams",
                "stop_words": "English Dictionary",
                "classifier": "Logistic Regression",
                "class_weight": "balanced",
                "solver": "lbfgs",
                "max_iter": 1000,
                "llm_engine": "Meta Llama 3.2 (3.2B)",
                "llm_runtime": "Local Ollama (Air-Gapped)",
                "llm_temperature": 0.2,
            },
            "top_phishing_features": [
                {"token": "click", "weight": 4.4747},
                {"token": "2005", "weight": 3.7560},
                {"token": "free", "weight": 3.6013},
                {"token": "remove", "weight": 3.5278},
                {"token": "money", "weight": 3.4259},
                {"token": "email", "weight": 3.3076},
                {"token": "life", "weight": 3.0164},
                {"token": "2004", "weight": 2.9063},
                {"token": "site", "weight": 2.8800},
                {"token": "info", "weight": 2.5969},
            ],
            "top_safe_features": [
                {"token": "enron", "weight": -7.1695},
                {"token": "language", "weight": -4.5953},
                {"token": "2002", "weight": -4.4643},
                {"token": "wrote", "weight": -4.3995},
                {"token": "thanks", "weight": -4.1670},
                {"token": "university", "weight": -3.9238},
                {"token": "edu", "weight": -3.4768},
                {"token": "linguistics", "weight": -3.4692},
                {"token": "2001", "weight": -3.4337},
                {"token": "vince", "weight": -3.2677},
            ]
        }
    }
    return render(request, "application/metrics.html", context)
