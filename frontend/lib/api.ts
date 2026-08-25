export type Product={slug:string;name:string;description:string;niche:string;product_type:string;price_cents:number;keywords:string[];faqs:{question:string;answer:string}[];related_slugs:string[]};
const base=process.env.API_BASE_URL||process.env.NEXT_PUBLIC_API_BASE_URL||'http://localhost:8000';
export async function products():Promise<Product[]>{const r=await fetch(`${base}/api/products`,{next:{revalidate:60}});return r.ok?r.json():[]}
export async function product(slug:string):Promise<Product|null>{const r=await fetch(`${base}/api/products/${encodeURIComponent(slug)}`,{cache:'no-store'});return r.ok?r.json():null}
