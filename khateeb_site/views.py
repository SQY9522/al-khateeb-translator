import json, os, tempfile
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

LANG_NAMES={
"ar":"العربية","en":"الإنجليزية","ur":"الأوردية","bn":"البنغالية","hi":"الهندية",
"ml":"المالايالامية","ta":"التاميلية","te":"التيلجو","sd":"السندية","ps":"البشتوية",
"fa":"الفارسية","ne":"النيبالية","id":"الإندونيسية","ms":"الملايوية","sw":"السواحيلية",
"so":"الصومالية","am":"الأمهرية","tr":"التركية","ku":"الكردية","uz":"الأوزبكية",
"tg":"الطاجيكية","ky":"القيرغيزية","az":"الأذرية"
}

def home(request):
    return render(request,"index.html",{"languages":LANG_NAMES})

def _client():
    from openai import OpenAI
    if not settings.OPENAI_API_KEY:
        return None
    return OpenAI(api_key=settings.OPENAI_API_KEY)

@csrf_exempt
def translate_text(request):
    if request.method!="POST":
        return JsonResponse({"error":"POST required"},status=405)
    try:
        data=json.loads(request.body.decode("utf-8"))
        text=(data.get("text") or "").strip()
        target=data.get("target","en")
        if not text:
            return JsonResponse({"text":""})
        if target=="ar":
            return JsonResponse({"text":text})
        if target not in LANG_NAMES:
            return JsonResponse({"error":"Unsupported language"},status=400)
        client=_client()
        if client is None:
            return JsonResponse({"error":"OPENAI_API_KEY is not configured."},status=503)
        prompt=f"""Translate the following Friday sermon excerpt from Arabic into {LANG_NAMES[target]}.
Return ONLY the translation, with no explanation, labels, notes, or quotation marks.
Preserve Islamic terms, Quran verses, hadith wording, honorifics, and names accurately. Do not invent content.
Arabic excerpt:
{text}"""
        response=client.responses.create(model=settings.OPENAI_TEXT_MODEL,input=prompt)
        return JsonResponse({"text":response.output_text.strip()})
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)

@csrf_exempt
def transcribe_audio(request):
    if request.method!="POST":
        return JsonResponse({"error":"POST required"},status=405)
    if not settings.OPENAI_API_KEY:
        return JsonResponse({"error":"OPENAI_API_KEY is not configured."},status=503)
    audio=request.FILES.get("audio")
    if not audio:
        return JsonResponse({"error":"No audio file."},status=400)
    client=_client()
    suffix=os.path.splitext(audio.name)[1] or ".webm"
    tmp=None
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=suffix) as f:
            for chunk in audio.chunks(): f.write(chunk)
            tmp=f.name
        with open(tmp,"rb") as fh:
            tr=client.audio.transcriptions.create(
                model=settings.OPENAI_TRANSCRIBE_MODEL,
                file=fh,
                language="ar",
                response_format="json"
            )
        return JsonResponse({"text":getattr(tr,"text","") or ""})
    except Exception as e:
        return JsonResponse({"error":str(e)},status=500)
    finally:
        if tmp:
            try: os.unlink(tmp)
            except OSError: pass
