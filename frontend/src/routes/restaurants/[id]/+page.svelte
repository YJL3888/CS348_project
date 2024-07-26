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
		GradientButton,
		Modal,
		Select,
		Textarea,
		Label,
		Dropdown,
		DropdownItem,
		Spinner
	} from 'flowbite-svelte';
	import {
		DotsHorizontalOutline,
		MessageDotsOutline,
		LinkedinSolid,
		GithubSolid,
		TwitterSolid
	} from 'flowbite-svelte-icons';
	import CommentItem from '$lib/CommentItem.svelte';

	export let data: PageData;

	let { restaurant } = data;

	function formatPrice(price: number) {
		return price.toFixed(2);
	}

	function getDiscountedPrice(itemId, originalPrice) {
		const today = new Date().toLocaleString('en-us', { weekday: 'short' }).toLowerCase();
		const applicableDiscounts = restaurant.discounts.filter(
			(d) => (d.item_id === itemId || d.item_id === null) && d.weekday === today
		);
		if (applicableDiscounts.length === 0) return { price: originalPrice, discounted: false };
		let newPrice = originalPrice;
		let discounted = false;
		for (const discount of applicableDiscounts) {
			if (discount.discount_type === '%') {
				newPrice -= (newPrice * discount.discount) / 100;
			} else {
				newPrice -= discount.discount;
			}
			discounted = true;
		}
		console.log(newPrice);
		return { price: newPrice, discounted };
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

	let formModal = false;

	function sendReview(e) {
		fetch('/api/review', {
			method: 'POST',
			body: new FormData(e.target)
		})
			.then((res) => {
				if (res.ok) return res.json();
				throw Error(res.statusText);
			})
			.then(
				(data) => {
					console.log(data);
					e.target.reset();
					formModal = false;
					restaurant.reviews = [data, ...restaurant.reviews];
				},
				(err) => {
					console.error(err);
				}
			);
	}

	let ratings = [
		{ value: 1, name: '1' },
		{ value: 2, name: '2' },
		{ value: 3, name: '3' },
		{ value: 4, name: '4' },
		{ value: 5, name: '5' }
	];

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

	async function deleteComment(id, par_id = null) {
		const res = await fetch('/api/comment/delete', {
			method: 'POST',
			body: new URLSearchParams({ comment_id: id })
		});
		if (res.ok) {
			if (par_id) {
				const parIdx = comments.findIndex((c) => c.id === par_id);
				comments[parIdx].replies = comments[parIdx].replies.filter((r) => r.id !== id);
			} else comments = comments.filter((c) => c.id !== id);
		}
	}
	function shareOnTwitter() {
		const url = encodeURIComponent(window.location.href);
		const text = encodeURIComponent(
			`Check out ${restaurant.restaurant_name}! ${restaurant.description}`
		);
		window.open(`https://twitter.com/intent/tweet?url=${url}&text=${text}`, '_blank');
	}

	function shareOnLinkedIn() {
		const url = window.location.href;
		const text = `Check out ${restaurant.restaurant_name}! ${restaurant.description} ${url}`;
		const shareUrl = `https://www.linkedin.com/feed/?shareActive=true&text=${encodeURIComponent(text)}`;
		window.open(shareUrl, '_blank');
	}

	function shareOnGitHub() {
		const githubRepoUrl = 'https://github.com/YJL3888/GooseGooseGo_CS348/blob/main/README.md';
		window.open(githubRepoUrl, '_blank');
	}
	function copyToClipboard() {
		const url = window.location.href;

		navigator.clipboard
			.writeText(url)
			.then(() => {
				alert('Link copied to clipboard');
			})
			.catch((err) => {
				console.error('Could not copy text: ', err);
			});
	}
</script>

<div class="container mx-auto max-w-[800px] p-6">
	<!-- Restaurant Details -->
	<h1 class="mb-4 text-3xl font-bold text-gray-900 dark:text-gray-100">
		{restaurant.restaurant_name}
	</h1>
	{#if restaurant.description}
		<p class="mb-6 text-lg text-gray-700 dark:text-gray-300">{restaurant.description}</p>
	{/if}
	<!-- Share to Social Media Buttons -->
	<div class="mb-6 flex space-x-2">
		<Button
			on:click={shareOnTwitter}
			class="flex items-center gap-2 rounded bg-blue-500 px-4 py-2 text-white"
		>
			<TwitterSolid class="h-5 w-5" /> Share on Twitter
		</Button>

		<Button
			on:click={shareOnLinkedIn}
			class="flex items-center gap-2 rounded bg-blue-600 px-4 py-2 text-white"
		>
			<LinkedinSolid class="h-5 w-5" /> Share on LinkedIn
		</Button>

		<Button
			on:click={shareOnGitHub}
			class="flex items-center gap-2 rounded bg-gray-800 px-4 py-2 text-white"
		>
			<GithubSolid class="h-5 w-5" /> Share on GitHub
		</Button>

		<Button
			on:click={copyToClipboard}
			class="flex items-center gap-2 rounded bg-gray-500 px-4 py-2 text-white"
		>
			Copy Link
		</Button>
	</div>

	<h2 class="mb-4 mt-4 text-2xl font-semibold text-gray-900 dark:text-gray-100">Menu</h2>
	<Table hoverable={true}>
		<TableHead>
			<TableHeadCell>Item Name</TableHeadCell>
			<TableHeadCell>Price</TableHeadCell>
		</TableHead>
		<TableBody tableBodyClass="divide-y">
			{#each restaurant.menu as item}
				<TableBodyRow>
					<TableBodyCell>{item.item_name}</TableBodyCell>
					<TableBodyCell>
						{@const discountCalc = getDiscountedPrice(item.item_id, item.Price)}
						{#if discountCalc.discounted}
							<s class="text-red-500">${formatPrice(item.Price)}</s>
							<span class="ml-2 text-green-500">${formatPrice(discountCalc.price)}</span>
						{:else}
							${formatPrice(item.Price)}
						{/if}
					</TableBodyCell>
				</TableBodyRow>
			{/each}
		</TableBody>
	</Table>

	{#if restaurant.discounts?.length}
		<h2 class="mb-4 mt-4 text-2xl font-semibold text-gray-900 dark:text-gray-100">Discounts</h2>
		<Table hoverable={true}>
			<TableHead>
				<TableHeadCell>Item Name</TableHeadCell>
				<TableHeadCell>Discount</TableHeadCell>
				<TableHeadCell>Day</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each restaurant.discounts as discount}
					<TableBodyRow>
						<TableBodyCell>
							{#if discount.item_id === null}
								All Items
							{:else}
								{#each restaurant.menu as item}
									{#if item.item_id === discount.item_id}
										{item.item_name}
									{/if}
								{/each}
							{/if}
						</TableBodyCell>
						<TableBodyCell>
							{discount.discount_type === '%'
								? `${formatPrice(discount.discount)}%`
								: `$${formatPrice(discount.discount)}`}
						</TableBodyCell>
						<TableBodyCell>{discount.weekday}</TableBodyCell>
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	{/if}

	<Tabs tabStyle="underline">
		<TabItem title="Reviews" open>
			{#if !restaurant.reviews.length}
				<p class="mb-5 text-gray-700 dark:text-gray-300">
					No reviews yet. Be the first to leave a review!
				</p>
			{/if}
			{#if data.user}
				<GradientButton color="pinkToOrange" on:click={() => (formModal = true)}
					>Write a review!</GradientButton
				>
				<Modal bind:open={formModal} size="xs" autoclose={false} outsideclose class="w-full">
					<form class="flex flex-col space-y-6" on:submit|preventDefault={sendReview}>
						<h3 class="mb-2 text-xl font-medium text-gray-900 dark:text-white">Leave a review!</h3>
						<Label class="space-y-2">
							<span>Select your rating</span>
							<Select class="mt-2" items={ratings} name="rating" required />
						</Label>
						<Label class="space-y-2">
							<span>Write your review</span>
							<Textarea
								id="review"
								rows="6"
								class="mb-4 resize-none"
								placeholder="Write a review..."
								name="comments"
								required
							></Textarea>
						</Label>
						<input type="hidden" name="restaurant_id" value={restaurant.restaurant_id} />
						<Button type="submit" class="w-full">Post Review</Button>
					</form>
				</Modal>
			{/if}
			{#if restaurant.reviews.length}
				<p class="mt-5" />
				{#each restaurant.reviews as review (review.review_id)}
					<RatingComment comment={formatReview(review)}>
						<p class="mb-2 whitespace-break-spaces font-light text-gray-500 dark:text-gray-400">
							{review.comments}
						</p>
					</RatingComment>
				{/each}
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
			{#each comments as comment, i (comment.id)}
				<CommentItem
					{comment}
					articleClass={i ? 'border-t border-gray-200 dark:border-gray-700 rounded-none' : ''}
					replyButton={!!data.user}
				>
					<svelte:fragment slot="dropdownMenu">
						{#if data.user?.sub === comment.commenter.id}
							<DotsHorizontalOutline class={`dots-menu-${comment.id} dark:text-white`} />
							<Dropdown triggeredBy={'.dots-menu-' + comment.id}>
								<DropdownItem on:click={(e) => deleteComment(comment.id)}>Delete</DropdownItem>
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
				{#each comment.replies as reply (reply.id)}
					<CommentItem comment={reply} articleClass="ml-6 lg:ml-12" replyButton={false}>
						<svelte:fragment slot="dropdownMenu">
							{#if data.user?.sub === reply.commenter.id}
								<DotsHorizontalOutline class={`dots-menu-${reply.id} dark:text-white`} />
								<Dropdown triggeredBy={'.dots-menu-' + reply.id}>
									<DropdownItem on:click={(e) => deleteComment(reply.id, comment.id)}
										>Delete</DropdownItem
									>
								</Dropdown>
							{/if}
						</svelte:fragment>
					</CommentItem>
				{/each}
			{/each}
		</TabItem>
	</Tabs>
</div>
