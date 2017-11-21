//
//  ViewController.swift
//  WTF
//
//  Created by 407195 on 2017. 11. 21..
//  Copyright © 2017년 407195. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, UIScrollViewDelegate {
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if section == 0 {
            return 1
        }
        
        return 10
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 2
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        if indexPath.section == 0 {
            let cell = tableView.dequeueReusableCell(withIdentifier: "mapcell")!
            return cell
        }
        
        let cell = tableView.dequeueReusableCell(withIdentifier: "infocell")!
        return cell
    }
    
    
    @IBOutlet weak var firstButton: UIButton!
    
    @IBOutlet weak var infoTableView: UITableView!
    
    @IBOutlet weak var buttonsContainer: UIView!
    override func viewDidLoad() {
        super.viewDidLoad()
        infoTableView.contentInset = UIEdgeInsetsMake(125, 0, 0, 0)
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func didClickeFirstButton(_ sender: UIButton) {
        print("iyan")
        self.firstButton.setTitle("우하하", for: .normal)
    }
    
    func reloadTable(){
        self.infoTableView.reloadData()
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat {
        if indexPath.section == 0 {
            return 400;
        }
        
        return 80;
    }
    
    func scrollViewDidScroll(_ scrollView: UIScrollView) {
         print(self.infoTableView.contentOffset.y)
        if self.infoTableView.contentOffset.y > -100 {
            self.buttonsContainer.alpha = 0;
        } else {
            self.buttonsContainer.alpha = 1;
        }
    }
}

