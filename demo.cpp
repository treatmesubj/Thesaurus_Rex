#include <iostream>
#include <string>

int main(int argc, char** argv)
{
    std::string args;
    for (int i = 1; i < argc; ++i) {
            args += argv[i];
            if (i != argc){
                args += " ";
            }
    }
    system(
        ("thesr.py " + args).c_str()
    );
    // system("pause");
}
