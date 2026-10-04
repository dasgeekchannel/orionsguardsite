// src/content.config.ts  Astro 5 content collection schema
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
	  type: 'content',
	  schema: z.object({
		      title: z.string(),
		      description: z.string().optional(),
		      // Accept either 'date' OR 'pubDate'  handles both our posts and old template files
		      date: z.coerce.date().optional(),
		      pubDate: z.coerce.date().optional(),
		      updatedDate: z.coerce.date().optional(),
		      tags: z.array(z.string()).default([]),
		      author: z.string().default("Orion's Guard"),
		      draft: z.boolean().default(false),
		      heroImage: z.string().optional(),
	  }),
});

export const collections = { blog };
