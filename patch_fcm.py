import re
content = open("supabase/functions/send-fcm/index.ts").read()

new_content = """import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import admin from "npm:firebase-admin@11.11.0"
import * as jose from "https://deno.land/x/jose@v4.14.4/index.ts"

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-firebase-token',
}

const JWKS_URL = 'https://www.googleapis.com/service_accounts/v1/jwk/securetoken@system.gserviceaccount.com'
const JWKS = jose.createRemoteJWKSet(new URL(JWKS_URL))

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  try {
    const firebaseToken = req.headers.get('x-firebase-token')
    if (!firebaseToken) {
      throw new Error('Missing x-firebase-token')
    }
        
    // Hardcoding as requested
    const FIREBASE_PROJECT_ID = 'appcodigo-7f245'
    
    // Validate the Firebase JWT 
    const { payload } = await jose.jwtVerify(firebaseToken, JWKS, {
      issuer: `https://securetoken.google.com/${FIREBASE_PROJECT_ID}`,
      audience: FIREBASE_PROJECT_ID,
    })
        
    // Check subject/uid
    if (!payload.sub) {
        throw new Error('Missing subject in token')
    }
        
    const email = payload.email as string
        
    if (email !== 'mestre@nrdlojas.com' && email !== 'admin@nrdlojas.com') {
        throw new Error('Unauthorized email: ' + email)
    }

    const { title, body, topic } = await req.json()
    
    if (!admin.apps.length) {
        const serviceAccountStr = Deno.env.get('FIREBASE_SERVICE_ACCOUNT')
        if (!serviceAccountStr) {
            throw new Error("Missing FIREBASE_SERVICE_ACCOUNT environment variable in Supabase.")
        }
        const serviceAccount = JSON.parse(serviceAccountStr)
        admin.initializeApp({
            credential: admin.credential.cert(serviceAccount)
        })
    }

    const response = await admin.messaging().send({
        topic: topic || 'products',
        notification: { title, body }
    })

    return new Response(
      JSON.stringify({ success: true, response }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 200 }
    )
  } catch (error) {
    console.error("FCM Error:", error)
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 400 }
    )
  }
})
"""
open("supabase/functions/send-fcm/index.ts", "w").write(new_content)
