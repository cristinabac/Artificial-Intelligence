from matrix_operations_final import get_transpose, matrix_mul, get_inverse
from random import shuffle


class Controller:

    def __init__(self):
        self.__data = []
        self.__data = self.read_data()

    def read_data(self):
        lst = []
        f = open("bdate2.txt", 'r')
        # primele 4 linii din fisier sunt inutile :D
        f.readline()
        f.readline()
        f.readline()
        f.readline()

        # prima instanta buna
        line = f.readline()
        # citesc si linia empty de dupa fiecare instance buna
        f.readline()

        while line != "":
            tok = line.split(' ')
            attr1 = float(tok[0])
            attr2 = float(tok[1])
            attr3 = float(tok[2])
            attr4 = float(tok[3])
            attr5 = float(tok[4])
            val = float(tok[5])
            inst = [attr1, attr2, attr3, attr4, attr5, val]
            lst.append(inst)

            # citesc urm linie, care va fi urmatoarea instanta
            line = f.readline()
            # citesc si linia goala inutila de dupa
            f.readline()

        return lst

    def get_training_data(self, data):
        """
        :param data:
        :return:
        """
        num = len(data) * 0.8
        return data[:int(num)]

    def get_test_data(self, data):
        """
        :param data:
        :return:
        """
        training = self.get_training_data(data)
        return data[len(training):]

    def get_statistics(self, coefficients, test_set, test_res):
        """
        Function to get statistics
        :param coefficients: coefficients of the linear function
        :param test_set: test_features
        :param test_res: test_results
        :return: statistics about predictions
        """
        # return matrix_mean(matrix_square_diff(matrix_mul(test_set, coefficients), test_res))

        squared = 0
        for test in range(len(test_set)):
            calculated_res = 0
            for i in range(len(coefficients)):
                calculated_res += coefficients[i][0] * test_set[test][i]
            squared += (calculated_res - test_res[test][0]) ** 2
            #print("Expected: " + str(test_res[test][0]) + " Predicted: " + str(calculated_res))
        return squared / len(test_set)

    def solve_least_squares(self, train_feat, res_feat):
        """
        Function to get the function coefficients
        :param res_feat: training result
        :param train_feat: training features
        :return:
        """

        training = train_feat

        result_training = res_feat

        trans = get_transpose(training)

        mat_mul_trans = matrix_mul(trans, training)

        mat_mul_trans = get_inverse(mat_mul_trans)

        second_prod = matrix_mul(mat_mul_trans, trans)

        return matrix_mul(second_prod, result_training)


    def run(self):

        shuffle(self.__data)

        features = []  # all features except the result
        result = []  # the result set

        for lst in self.__data:
            features.append([1, lst[0], lst[1], lst[2], lst[3], lst[4]])  # ACEL 1 E FOARTE IMPORTANT !!!!!!!!!!! :D
            result.append([lst[5]])

        training_features = self.get_training_data(features)  # 80% of features (for training)
        result_features = self.get_training_data(result)  # 80% of results (for training)
        test_features = self.get_test_data(features)  # 20% of features (for test)
        result_test = self.get_test_data(result)  # 20% of results (for test)


        coeffs = self.solve_least_squares(training_features, result_features)
        print("Mean squared error for least squares method: " + str(self.get_statistics(coeffs, test_features, result_test)))
        print("Least squared coefficients calculated: " + str(coeffs))

        return self.get_statistics(coeffs, test_features, result_test)


def main():
    err_sum = 0
    err_cnt = 0

    c = Controller()

    for i in range(10):
        print()
        print("RULAREA NUMARUL ", i)
        err = c.run()
        err_sum += err
        err_cnt += 1

    print()
    print("Pentru 10 rulari, eroarea medie:")
    print(err_sum/err_cnt)

main()


