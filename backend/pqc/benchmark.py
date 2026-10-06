from __future__ import annotations
import time
def benchmark_liboqs(iterations:int=5)->list[dict]:
    try: import oqs
    except Exception as exc: return [{"status":"unavailable","reason":str(exc),"hint":"Install liboqs-python and native liboqs for the optional PQC lab."}]
    results=[]
    for alg in ["ML-KEM-768","ML-DSA-65"]:
        try:
            if "KEM" in alg:
                start=time.perf_counter()
                for _ in range(iterations):
                    with oqs.KeyEncapsulation(alg) as kem: public_key=kem.generate_keypair()
                keygen_ms=(time.perf_counter()-start)*1000/iterations
                with oqs.KeyEncapsulation(alg) as kem:
                    public_key=kem.generate_keypair(); start=time.perf_counter(); ct,ss=kem.encap_secret(public_key); enc_ms=(time.perf_counter()-start)*1000
                    start=time.perf_counter(); kem.decap_secret(ct); dec_ms=(time.perf_counter()-start)*1000
                    results += [{"status":"ok","algorithm":alg,"operation":"keygen","elapsed_ms":keygen_ms,"public_key_bytes":len(public_key)},{"status":"ok","algorithm":alg,"operation":"encapsulation","elapsed_ms":enc_ms,"signature_or_ciphertext_bytes":len(ct)},{"status":"ok","algorithm":alg,"operation":"decapsulation","elapsed_ms":dec_ms}]
            else:
                start=time.perf_counter()
                for _ in range(iterations):
                    with oqs.Signature(alg) as sig:
                        public_key,secret_key=sig.generate_keypair(); sig.sign(b"CyberFusion PQC benchmark")
                total_ms=(time.perf_counter()-start)*1000/iterations
                results.append({"status":"ok","algorithm":alg,"operation":"keypair+sign","elapsed_ms":total_ms,"public_key_bytes":len(public_key),"private_key_bytes":len(secret_key)})
        except Exception as exc: results.append({"status":"error","algorithm":alg,"reason":str(exc)})
    return results
