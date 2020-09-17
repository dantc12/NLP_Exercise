import gzip
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Number of reviews: 7,911,684
TOTAL_REVIEWS = 7911684
# Number of users: 889,176
TOTAL_USERS = 889176
# Number of products: 253,059
# Users with over 50 reviews: 16,341
# Median no. of words per review: 101
# Timespan: Aug 1997 - Oct 2012

FILE_PATH = 'movies.txt.gz'
ENCODING = 'latin1'
REVIEW_USEFUL_FEATURES = ['productId', 'helpfulness', 'score', 'time', 'summary', 'text']


class ReviewData:
    def __init__(self, data_file_path, max_users=TOTAL_USERS, max_reviews=TOTAL_REVIEWS):
        self._data_file_path = data_file_path

        self._n_reviews = 0
        self._n_users = 0
        self._max_reviews = max_reviews
        self._max_users = max_users

        self._userIds = []
        self._userReviews = []

        self._populate_data(data_file_path)

    def _populate_data(self, data_file):
        logging.debug('Starting population of {} users\'s reviews from {} reviews in file.'.format(self._max_users, self._max_reviews))
        with gzip.open(data_file, 'rt', encoding=ENCODING) as f:
            data_point = dict()
            for line in f:
                if line == "\n":
                    self._add_review(data_point)
                    self._n_reviews += 1
                    if self._n_reviews == self._max_reviews:
                        break
                    data_point = dict()
                else:
                    feature_name = ''.join(line.split(':')[0].split('/')[1:])
                    data_point[feature_name] = ' '.join(line.split(' ')[1:]).strip('\n')

        logging.debug('Populated data structure successfully.')

    def _add_review(self, data_point):
        userId = data_point.get('userId')

        try:
            user_index = self._userIds.index(userId)
            self._userReviews[user_index].append(data_point)
        except ValueError:
            if self._n_users < self._max_users:
                self._userIds.append(userId)
                self._userReviews.append([data_point])
                self._n_users += 1
            else:
                return

    def get_users_list(self):
        return self._userIds

    def get_total_reviews(self):
        return self._n_reviews

    def get_user_reviews(self, userId):
        logging.debug('Starting search for user reviews.')
        user_index = self._userIds.index(userId)

        n_user_reviews = len(self._userReviews[user_index])
        logging.debug('Returning user {}\'s  {} reviews.'.format(userId, n_user_reviews))
        return self._userReviews[user_index]

    def get_all_reviews(self):
        logging.debug('Starting retrieval of all user reviews.')
        res = [item for sublist in self._userReviews for item in sublist]
        logging.debug('Done')
        return res


if __name__ == "__main__":
    review_data = ReviewData(FILE_PATH, 4)
    users = review_data.get_users_list()
    # print(users)
    user = users[3]
    user_reviews = review_data.get_user_reviews(user)

