def calc_user_sim(self):
	// 构建物品-用户倒排表
	movie2users = dict()
	for user, movies in self.trainset.items():
		for movie in movies:
			if movie not in movie2users:
				movie2users[movie] = set()
			movie2users[movie].add(user)
			if movie not in self.movie_popular:
				self.movie_popular[movie] = 0
			self.movie_popular[movie] += 1

	// 计算两两用户之前的共同评价电影数
	usersim_mat = self.user_sim_mat
	for movie, users in movie2users.items():
		for u in users:
			for v in users:
				if u == v:
					continue
				usersim_mat.setdefault(u, {})
				usersim_mat[u].setdefault(v, 0)
				usersim_mat[u][v] += 1

	// 计算用户兴趣相似度
	for u, related_users in usersim_mat.items():
		for v, count in related_users.items():
			usersim_mat[u][v] = count / math.sqrt(len(self.trainset[u]) * len(self.trainset[v]))