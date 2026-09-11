import json, os, tempfile
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

LANG_NAMES={"ar":"العربية","en":"الإنجليزية","ur":"الأوردية","bn":"البنغالية","hi":"الهندية","ml":"المالايالامية","ta":"التاميلية","te":"التيلجو","sd":"السندية","ps":"البشتوية","fa":"الفارسية","ne":"النيبالية","id":"الإندونيسية","ms":"الملايوية","sw":"السواحيلية","so":"الصومالية","am":"الأمهرية","tr":"التركية","ku":"الكردية","uz":"الأوزبكية","tg":"الطاجيكية","ky":"القيرغيزية","az":"الأذرية"}

def home(request): return render(request,"index.html",{"languages":json.dumps(LANG_NAMES,ensure_ascii=False)})

def _client():
    from openai import OpenAI
    key=settings.OPENAI_API_KEY.strip()
    return OpenAI(api_key=key) if key else None

@csrf_exempt
def translate_text(request):
    if request.method!="POST": return JsonResponse({"error":"POST required"},status=405)
    try:
        data=json.loads(request.body.decode("utf-8")); text=(data.get("text") or "").strip(); target=data.get("target","en")
        if not text: return JsonResponse({"text":""})
        if target=="ar": return JsonResponse({"text":text})
        if target not in LANG_NAMES: return JsonResponse({"error":"Unsupported language"},status=400)
        client=_client()
        if client is None: return JsonResponse({"error":"OPENAI_API_KEY is not configured on the server."},status=503)
        response=client.responses.create(model=settings.OPENAI_TEXT_MODEL,input=f"Translate this Friday sermon excerpt from Arabic into {LANG_NAMES[target]}. Return only the translation. Preserve Quran, hadith, Islamic terminology, names and honorifics accurately. Do not add explanations.\n\n{text}")
        out=(response.output_text or "").strip()
        if not out: return JsonResponse({"error":"The translation service returned no text."},status=502)
        return JsonResponse({"text":out})
    except Exception as e:
        return JsonResponse({"error":f"Translation service error: {str(e)}"},status=502)

@csrf_exempt
def transcribe_audio(request):
    if request.method!="POST": return JsonResponse({"error":"POST required"},status=405)
    if not settings.OPENAI_API_KEY: return JsonResponse({"error":"OPENAI_API_KEY is not configured on the server."},status=503)
    audio=request.FILES.get("audio")
    if not audio: return JsonResponse({"error":"No audio file."},status=400)
    client=_client(); tmp=None
    try:
        suffix=os.path.splitext(audio.name)[1] or ".webm"
        with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as f:
            for chunk in audio.chunks(): f.write(chunk)
            tmp=f.name
        with open(tmp,"rb") as fh:
            tr=client.audio.transcriptions.create(model=settings.OPENAI_TRANSCRIBE_MODEL,file=fh,language="ar",response_format="json")
        return JsonResponse({"text":getattr(tr,"text","") or ""})
    except Exception as e: return JsonResponse({"error":f"Transcription service error: {str(e)}"},status=502)
    finally:
        if tmp:
            try: os.unlink(tmp)
            except OSError: pass
