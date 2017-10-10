"""
Banks
-----

Interface to manage bank accounts.
"""
from enum import Enum

import pytest


class AccountType(Enum):
    SAVINGS = 1
    CHECKING = 2


class BankAccount():
    def __init__ (self, owner, accountType):
        """ Init balance to 0. """
        self.owner = owner
        self.accountType = accountType
        self.balance = 0

    def withdraw (self, amount):
        if self.balance < amount:
            raise ValueError('Cannot withdraw more than current balance.')
        if amount < 0:
            raise ValueError('Cannot withdraw negative amount.')

        self.balance -= amount

    def deposit (self, amount):
        if amount < 0:
            raise ValueError('Cannot deposit negative amount.')

        self.balance += amount

    def __str__ (self):
        return 'Type: {0}\nOwner: {1}\nBalance: {2:.2f}'.format(
              self.accountType.name, self.owner, self.balance)

    def __len__ (self):
        return self.balance


class BankUser():
    def __init__ (self, owner):
        self.owner = owner
        self.accounts = {}

    def addAccount (self, accountType):
        """ Raises ValueError if user already has an account of this type. """
        if len(self.accounts) > 0:
            if accountType in self.accounts:
                raise ValueError('Only one {} account per user.'.format(
                      accountType.name))

        new_account = BankAccount(self.owner, accountType)
        self.accounts[accountType] = new_account

    def getBalance (self, accountType):
        if accountType not in self.accounts:
            raise ValueError('{0} has no {1} account.'.format(
                  self.owner, accountType.name))

        return self.accounts[accountType].balance

    def deposit (self, accountType, amount):
        if accountType not in self.accounts:
            raise ValueError('{0} has no {1} account.'.format(
                  self.owner, accountType.name))

        self.accounts[accountType].deposit(amount)

    def withdraw (self, accountType, amount):
        if accountType not in self.accounts:
            raise ValueError('{0} has no {1} account.'.format(
                  self.owner, accountType.name))

        self.accounts[accountType].withdraw(amount)

    def __str__ (self):
        msg = '{} has '.format(self.owner)
        if len(self.accounts) == 0:
            msg += 'no accounts.'
            return msg

        if len(self.accounts) == 1:
            msg += '1 account.'
        else:
            msg += '{} accounts.'.format(len(self.accounts))

        for i, acct in self.accounts.items():
            msg += '\n' + '-' * 20 + '\n'  # divider
            msg += str(acct)

        return msg


def ATMSession (bankUser):
    """ Returns closure method providing session for BankUser class. """

    def Interface ():
        def get_main_user_option ():
            option_request = 'Enter Option:\n\n1)Exit\n2)Create Account\n3)Check ' \
                             'Balance\n4)Deposit\n5)Withdraw\n'
            try:
                response = int(input(option_request))
            except:
                print('Retrying due to invalid command.\n')
                return get_main_user_option()
            else:
                if response in [1, 2, 3, 4, 5]:
                    return response
                print('Retrying due to invalid response number.\n')
                return get_main_user_option()

        def get_account_type ():
            option_request = 'Enter Option:\n1)Checking\n2)Savings\n'
            try:
                response = int(input(option_request))
            except:
                print('Retrying due to invalid command.\n')
                return get_account_type()

            if response == 1:
                return AccountType.SAVINGS
            elif response == 2:
                return AccountType.CHECKING
            else:
                print('Invalid account type provided. Retrying.\n')
                return get_account_type()

        def get_int_amount ():
            try:
                response = int(input('Enter Integer Amount, Cannot Be Negative:\n'))
            except:
                print('Retrying due to invalid integer amount.\n')
                return get_int_amount()
            else:
                if response >= 0:
                    return response
                print('Amount cannot be negative.\n')
                return get_int_amount()

        while True:
            option = get_main_user_option()

            if option == 1:
                break

            if option == 2:
                acct_type = get_account_type()
                bankUser.addAccount(acct_type)
                print('Account added\n')

            if option == 3:
                acct_type = get_account_type()
                balance = bankUser.getBalance(acct_type)
                print('Balance = {:.2f}\n'.format(balance))

            if option == 4:
                acct_type = get_account_type()
                amount = get_int_amount()
                try:
                    bankUser.deposit(acct_type, amount)
                except Exception as e:
                    print(e)

            if option == 5:
                acct_type = get_account_type()
                amount = get_int_amount()
                try:
                    bankUser.withdraw(acct_type, amount)
                except Exception as e:
                    print(e)

    return Interface

if __name__ == '__main__':
    def test_withdraw_more_than_balance ():
        user = BankUser('George Nelson')
        user.addAccount(AccountType.CHECKING)
        user.deposit(AccountType.CHECKING, 1000)
        with pytest.raises(ValueError, message='Expecting ValueError'):
            user.withdraw(AccountType.CHECKING, 1005)


    def test_deposit_negative_amount ():
        user = BankUser('George Nelson')
        user.addAccount(AccountType.CHECKING)
        with pytest.raises(ValueError, message='Expecting ValueError'):
            user.deposit(AccountType.CHECKING, -200)


    def test_getBalance ():
        """ Ensure balance after several deposits/withdrawals is what expected. """
        user = BankUser('George Nelson')
        user.addAccount(AccountType.SAVINGS)
        user.deposit(AccountType.SAVINGS, 5000)
        user.withdraw(AccountType.SAVINGS, 2000)
        user.deposit(AccountType.SAVINGS, 500)
        assert user.getBalance(AccountType.SAVINGS) == 3500


    def test_user_str ():
        """ Ensure expected parts of string representation are present. """
        user = BankUser('George Nelson')
        user.addAccount(AccountType.SAVINGS)
        user.deposit(AccountType.SAVINGS, 10)
        summary = str(user)
        assert 'SAVINGS' in summary
        assert 'George Nelson' in summary
        assert '10.00' in summary


    # Run tests on BankUser.
    test_withdraw_more_than_balance()
    test_deposit_negative_amount()
    test_getBalance()
    test_user_str()

    # Demo ATMSession closure method.
    user = BankUser('George Nelson')
    session = ATMSession(user)
    session()