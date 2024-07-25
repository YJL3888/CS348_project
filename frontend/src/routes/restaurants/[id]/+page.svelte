<script lang="ts">
	import type { PageData } from './$types';
	import {
		Table,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		TableHead,
		TableHeadCell,
		RatingComment,
		Tabs,
		TabItem,
		Button,
		Textarea,
		Label,
		Dropdown,
		DropdownItem,
		Spinner,
		GradientButton
	} from 'flowbite-svelte';
	import { DotsHorizontalOutline, MessageDotsOutline } from 'flowbite-svelte-icons';
	import CommentItem from '$lib/CommentItem.svelte';

	export let data: PageData;

	let { restaurant } = data;

	function formatPrice(price: number) {
		return price.toFixed(2);
	}

	function formatReview(review) {
		return {
			id: review.review_id,
			user: {
				name: review.username,
				img: {
					src: '/images/goose.png', // Placeholder image, replace with actual user images if available
					alt: 'User profile image'
				},
				joined: new Date(review.timestamp).toLocaleString() // Placeholder, replace with actual user joined date if available
			},
			total: 5,
			rating: review.rating
			//heading: review.comments // Use comments as heading
			//address: 'N/A', // Placeholder, replace with actual user address if available
			//datetime: review.timestamp // Use review timestamp
		};
	}

	let comments = [];

	const adjustComment = (comment) => ({
		id: comment.comment_id,
		commenter: {
            id: comment.user_id,
			name: comment.username,
			profilePicture: '/images/goose.png'
		},
		date: new Date(comment.posted_time).toLocaleString(),
		content: comment.content,
		replies: []
	});

	$: {
		const lookup = new Map();
		const newComments = [];
		for (const comment of restaurant.comments) {
			const adjustedComment = adjustComment(comment);
			(comment.parent_comment_id
				? lookup.get(comment.parent_comment_id).replies
				: newComments
			).push(adjustedComment);
			lookup.set(comment.comment_id, adjustedComment);
		}
        for (const comment of newComments) comment.replies.reverse();
		comments = newComments.reverse();
	}

	let comments_info = {};

	async function handleComment(e, id) {
		(comments_info[id] ??= {}).submitting = true;
		comments_info[id].error = false;
		try {
			const res = await fetch('/api/comment', {
				method: 'POST',
				body: new FormData(e.target)
			});
			if (!res.ok) {
				comments_info[id].error = true;
				return;
			}
			const data = await res.json();
			if (~id) {
				const parIdx = comments.findIndex((c) => c.id === id);
				comments[parIdx].replies = [adjustComment(data), ...comments[parIdx].replies];
			} else comments = [adjustComment(data), ...comments];
			comments_info[id].replying = false;
		} catch (err) {
			comments_info[id].error = true;
		} finally {
			comments_info[id].submitting = false;
		}
	}

	function closeReplyBox(id) {
		comments_info[id].replying = false;
		comments_info[id].error = false;
	}
</script>

<div class="container mx-auto max-w-[800px] p-6">
	<!-- Restaurant Details -->
	<h1 class="mb-4 text-3xl font-bold text-gray-900 dark:text-gray-100">
		{restaurant.restaurant_name}
	</h1>
	<p class="mb-6 text-lg text-gray-700 dark:text-gray-300">{restaurant.description}</p>

	<h2 class="mb-4 text-2xl font-semibold text-gray-900 dark:text-gray-100">Menu</h2>
	<Table hoverable={true}>
		<TableHead>
			<TableHeadCell>Item Name</TableHeadCell>
			<TableHeadCell>Price</TableHeadCell>
		</TableHead>
		<TableBody tableBodyClass="divide-y">
			{#each restaurant.menu as item}
				<TableBodyRow>
					<TableBodyCell>{item.item_name}</TableBodyCell>
					<TableBodyCell>${formatPrice(item.Price)}</TableBodyCell>
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>

	<Tabs tabStyle="underline">
		<TabItem title="Reviews" open>
			{#if restaurant.reviews.length > 0}
				{#each restaurant.reviews as review}
					<RatingComment comment={formatReview(review)}>
						<p class="mb-2 font-light text-gray-500 dark:text-gray-400">{review.comments}</p>
					</RatingComment>
				{/each}
			{:else}
				<p class="text-gray-700 dark:text-gray-300">
					No reviews yet. Be the first to leave a review!
				</p>
			{/if}
		</TabItem>
		<TabItem title={'Comments (' + comments.length + ')'}>
			{#if data.user}
				<form class="mb-6" on:submit|preventDefault={(e) => handleComment(e, -1)}>
					<Label for="comment" class="sr-only">Your comment</Label>
					<Textarea
						id="comment"
						rows="6"
						class="mb-4 resize-none"
						placeholder="Write a comment..."
						name="content"
						required
					></Textarea>
					<Button type="submit" class="px-4 text-xs font-medium">
						{#if comments_info[-1]?.submitting}
							<Spinner class="me-3" size="4" color="white" />
						{/if}
						Post comment
					</Button>
					<input type="hidden" name="restaurant_id" value={restaurant.restaurant_id} />
					{#if comments_info[-1]?.error}
						<p class="text-red-500">
							An error occurred while posting your comment. Please try again later.
						</p>
					{/if}
				</form>
			{/if}
			{#each comments as comment, i}
				<CommentItem
					{comment}
					articleClass={i !== 0 ? 'border-t border-gray-200 dark:border-gray-700 rounded-none' : ''}
					replyButton={!!data.user}
				>
					<svelte:fragment slot="dropdownMenu">
						{#if data.user?.sub === comment.commenter.id}
							<DotsHorizontalOutline class={`dots-menu-${comment.id} dark:text-white`} />
							<Dropdown triggeredBy={'.dots-menu-' + comment.id}>
								<DropdownItem>Delete</DropdownItem>
							</Dropdown>
						{/if}
					</svelte:fragment>
					<svelte:fragment slot="reply">
						<div class="mt-4 flex items-center space-x-4">
							<button
								type="button"
								class="flex items-center text-sm text-gray-500 hover:underline dark:text-gray-400"
								on:click={(e) => ((comments_info[comment.id] ??= {}).replying = true)}
							>
								<MessageDotsOutline class="mr-1 h-4 w-4" />
								Reply
							</button>
						</div>
						{#if comments_info[comment.id]?.replying}
							<form class="mt-6" on:submit|preventDefault={(e) => handleComment(e, comment.id)}>
								<input type="hidden" name="parent_comment_id" value={comment.id} />
								<input type="hidden" name="restaurant_id" value={restaurant.restaurant_id} />
								<Label for={'comment_' + comment.id} class="sr-only">Your comment</Label>
								<Textarea
									id={'comment_' + comment.id}
									rows="6"
									class="mb-4 resize-none"
									placeholder="Write a reply..."
									name="content"
									required
								></Textarea>
								<div class="flex flex-wrap gap-2">
									<GradientButton type="submit" class="px-4 text-xs font-medium" color="green">
										{#if comments_info[comment.id]?.submitting}
											<Spinner class="me-3" size="4" color="white" />
										{/if}
										Post comment
									</GradientButton>
									<GradientButton color="red" on:click={(e) => closeReplyBox(comment.id)}>
										Cancel
									</GradientButton>
								</div>
								<input type="hidden" name="restaurant_id" value={restaurant.restaurant_id} />
								{#if comments_info[comment.id]?.error}
									<p class="text-red-500">
										An error occurred while posting your comment. Please try again later.
									</p>
								{/if}
							</form>
						{/if}
					</svelte:fragment>
				</CommentItem>
				{#each comment.replies as reply}
					<CommentItem comment={reply} articleClass="ml-6 lg:ml-12" replyButton={false}>
                        <svelte:fragment slot="dropdownMenu">
                            {#if data.user?.sub === reply.commenter.id}
                                <DotsHorizontalOutline class={`dots-menu-${comment.id} dark:text-white`} />
                                <Dropdown triggeredBy={'.dots-menu-' + comment.id}>
                                    <DropdownItem>Delete</DropdownItem>
                                </Dropdown>
                            {/if}
                        </svelte:fragment>
                    </CommentItem>
				{/each}
			{/each}
		</TabItem>
	</Tabs>
</div>
