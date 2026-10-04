// src/content.config.ts — Astro 5 content collection schema
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    author: z.string().default("Orion's Guard"),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };
