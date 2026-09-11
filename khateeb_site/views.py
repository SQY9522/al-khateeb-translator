import json
import os
import threading

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

SUPPORTED_LANGS={"ar","en","ur","bn","hi","ml","ta","sd","ps","fa","ne","id","ms","sw","so","am","tr","uz","az"}

LANG_NAMES={"ar":"العربية","en":"الإنجليزية","ur":"الأوردية","bn":"البنغالية","hi":"الهندية","ml":"المالايالامية","ta":"التاميلية","sd":"السندية","ps":"البشتوية","fa":"الفارسية","ne":"النيبالية","id":"الإندونيسية","ms":"الملايوية","sw":"السواحيلية","so":"الصومالية","am":"الأمهرية","tr":"التركية","uz":"الأوزبكية","az":"الأذرية"}

HADITH = "«مَن توضأ فأحسن الوضوء، ثم أتى الجمعة، فاستمع وأنصت، غُفر له ما بينه وبين الجمعة، وزيادة ثلاثة أيام، ومن مس الحصى فقد لغا.»"

# Argos v2 ships a multilingual M2M100 model. It covers many of the languages
# used by the site and can translate directly from Arabic without a paid API.
ARGOS_MODEL_PATH = os.path.join(os.getenv("ARGOS_MODEL_DIR", ".argos"), "translate-fairseq_m2m_100_418M.argosmodel")
_argos_lock = threading.Lock()
_argos_ready = False

def home(request):
    return render(request, "index.html", {"languages": json.dumps(LANG_NAMES, ensure_ascii=False)})

def _argos():
    global _argos_ready
    import argostranslate.package
    import argostranslate.translate

    with _argos_lock:
        if _argos_ready:
            return argostranslate.translate

        if os.path.exists(ARGOS_MODEL_PATH):
            try:
                argostranslate.package.install_from_path(ARGOS_MODEL_PATH)
            except Exception:
                # It may already be installed from the build step.
                pass
        _argos_ready = True
        return argostranslate.translate

def _translate(text, target):
    if target == "ar":
        return text
    if target not in LANG_NAMES:
        raise ValueError("Unsupported language")
    if target not in SUPPORTED_LANGS:
        raise ValueError("هذه اللغة غير متاحة حاليًا في النموذج المجاني")
    translator = _argos()
    result = translator.translate(text, "ar", target)
    return (result or "").strip()

@csrf_exempt
def translate_text(request):
    if request.method != "POST":
        return JsonResponse({"error":"POST required"}, status=405)
    try:
        data=json.loads(request.body.decode("utf-8"))
        text=(data.get("text") or "").strip()
        target=data.get("target", "en")
        if not text:
            return JsonResponse({"text":""})
        return JsonResponse({"text":_translate(text, target)})
    except ValueError as e:
        return JsonResponse({"error":str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error":f"Translation service error: {str(e)}"}, status=502)

@csrf_exempt
def translate_hadith(request):
    if request.method != "POST":
        return JsonResponse({"error":"POST required"}, status=405)
    try:
        data=json.loads(request.body.decode("utf-8"))
        target=data.get("target", "en")
        return JsonResponse({"text":_translate(HADITH, target)})
    except ValueError as e:
        return JsonResponse({"error":str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error":f"Hadith translation error: {str(e)}"}, status=502)
